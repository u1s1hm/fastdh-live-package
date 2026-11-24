from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def tables():
    text = (ROOT/'references/interaction-tables.md').read_text(encoding='utf-8')
    result = []
    for block in text.split('\n\n'):
        lines = block.splitlines()
        if lines and lines[0].startswith('| Rule ID |'):
            cells = lambda line: [v.strip() for v in line.strip('|').split('|')]
            header = cells(lines[0])
            rows = []
            for line in lines[2:]:
                values = cells(line)
                assert len(values) == len(header)
                rows.append(dict(zip(header, values)))
            result.append((header, rows))
    return result

def render(header, rows):
    return '\n'.join(['| ' + ' | '.join(header) + ' |',
                     '| ' + ' | '.join(['---']*len(header)) + ' |'] +
                    ['| ' + ' | '.join(row[h] for h in header) + ' |' for row in rows])

class HandoffTables(unittest.TestCase):
    def check_variant(self, ids):
        (rh, rules), (sh, steps) = tables()
        rules = [dict(r) for r in rules if r['Rule ID'] in ids]
        steps = [dict(s) for s in steps if s['Rule ID'] in ids]
        for n, rule in enumerate(rules, 1):
            rule['Order'] = str(n)
            self.assertEqual(rule['Enabled'], 'true')
            linked = [s for s in steps if s['Rule ID'] == rule['Rule ID']]
            self.assertTrue(1 <= len(linked) <= 8)
            self.assertEqual([int(s['Step']) for s in linked], list(range(1,len(linked)+1)))
        self.assertEqual({s['Rule ID'] for s in steps}, set(ids))
        for row in rules+steps:
            self.assertTrue(all(row.values()))
        for s in steps:
            if s['Action'] == 'Switch template':
                self.assertEqual(s['Template mode'], 'Fixed category')
                self.assertEqual(s['Template category'], 'demo_base')
                self.assertEqual(s['Switch trigger'], 'N/A')
                self.assertEqual(s['Required switch'], 'true')
            else:
                self.assertEqual(s['Action'], 'Generate reply')
                self.assertEqual(s['Spoken language'], 'English')
                self.assertIn('Answer the current comment',s['Text or prompt'])
        # Render complete Markdown tables, then verify data row count and cell width.
        for header, rows in ((rh,rules),(sh,steps)):
            output = render(header,rows)
            self.assertEqual(len(output.splitlines()),len(rows)+2)
            for line in output.splitlines():
                self.assertEqual(len(line.strip('|').split('|')),len(header))
        return rules, steps

    def test_dual(self):
        rules,_ = self.check_variant(['R01','R02'])
        self.assertEqual([r['Rule ID'] for r in rules],['R01','R02'])
    def test_reply_only(self): self.check_variant(['R02'])
    def test_switch_only(self): self.check_variant(['R01'])
    def test_none(self): self.check_variant([])
    def test_substring_not_exact(self):
        # Contract expectation, not a FastDH emulator or live-platform test.
        actual = {x: '111' in x for x in ['111','1111','hi111','Hello']}
        self.assertEqual(actual, {'111':True,'1111':True,'hi111':True,'Hello':False})
        exact = {x:x=='111' for x in actual}
        self.assertEqual([x for x in actual if actual[x]!=exact[x]], ['1111','hi111'])
    def test_existing_indexer(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('idx',ROOT/'scripts/script_index.py')
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        en=mod.index_script('Hello.\nAgain.\n[Configuration | U01 end] END')
        zh=mod.index_script('你好。\n【配置说明｜U01结束】结束')
        self.assertEqual(en['status'],zh['status'])
        self.assertEqual(en['sections'][0]['spoken_end'],2)
        self.assertEqual(zh['sections'][0]['spoken_end'],1)

if __name__ == '__main__': unittest.main()
