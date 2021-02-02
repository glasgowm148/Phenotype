# -*- coding: utf-8 -*-

import csv
import os

import pdfkit
import yaml
from jinja2 import Environment, FileSystemLoader


class GenomeReport():
    """Genome report."""

    conf = {}
    report = {}
    snp = {}
    genoma_data = {}

    def __init__(self, genome_file,
                 report_format='html',
                 output='my_report', lang='es'):
        """Init."""
        self.conf = {
            'genome_file': genome_file,
            'report_format': report_format,
            'output_name': output,
            'report': 'data/{}/report.yml'.format(lang),
            'snp': 'data/{}/snp.yml'.format(lang)
        }
        self.load_files()

    def render(self, context, template='template/report.html'):
        """Make report to html."""
        path, filename = os.path.split(template)
        result = Environment(
            loader=FileSystemLoader(path or './')).get_template(
            filename).render(context)
        open('{}.html'.format(self.conf['output_name']), 'w').write(result)
        if self.conf['report_format'] == 'pdf':
            pdfkit.from_file(
                '{}.html'.format(self.conf['output_name']),
                '{}.pdf'.format(self.conf['output_name']))
            os.system('rm {}.html'.format(self.conf['output_name']))

    def load_files(self):
        """Load all files YAML and CSV."""
        self.report = yaml.load(open(self.conf['report'], 'r').read())
        self.snp = yaml.load(open(self.conf['snp'], 'r').read())
        self.genoma_data = list(
            csv.reader(open(self.conf['genome_file'], 'r'), delimiter='\t'))
        self.genoma_data = [x for x in self.genoma_data if len(x) == 4][1:]
        data_tmp = {}
        for data in self.genoma_data:
            data_tmp[data[0]] = [data[1], data[3]]
        self.genoma_data = data_tmp

    def search_alelo(self, genotype_results, g):
        """Detect alelo for example -C."""
        if '-' in g:
            g = g.replace('-', '')
        for genotype in genotype_results.keys():
            if '-' in genotype:
                alelo = genotype.replace('-', '')
                if len(alelo) == 1:
                    if alelo == g or alelo == g[::-1]:
                        return genotype_results[genotype]
        return False

    def _count_good_bad(self, good, bad, result):
        if result is not None:
            if result is True:
                good += 1
            elif result is False:
                bad += 1
        return good, bad

    def _check_repute(self, good, bad):
        if good > bad:
            return True
        elif bad > good:
            return False

    def _make_return(self, result, good, bad, total):
        if len(result) <= 0:
            return dict(snp=False, repute=False,
                        good=good, bad=bad, total=total)
        repute = self._check_repute(good, bad)
        return dict(snp=result, repute=repute,
                    good=good, bad=bad, total=total)

    def _check_snp(self, snp_list):
        result = []
        good = bad = total = 0
        for snp in snp_list:
            genotype_info = self.genoma_data.get(snp, False)
            if genotype_info:
                genotype_results = self.snp.get(snp, False)
                if genotype_results:
                    result_info = genotype_results.get(genotype_info[1], False)
                    if not result_info:
                        result_info = self.search_alelo(
                            genotype_results, genotype_info[1])
                    if result_info:
                        result.append({
                            'snp': snp, 'chromosome': genotype_info[0],
                            'genotype': genotype_info[1],
                            'info': result_info[0], 'repute': result_info[1]})
                        good, bad = self._count_good_bad(
                            good, bad, result_info[1])
                        total += 1
        return self._make_return(result, good, bad, total)

    def make_report(self):
        """Create custom report."""
        result = {}
        for category in self.report:
            category_data = self.report[category]
            result[category] = {'title': category_data['title'],
                                'icon': category_data['icon'],
                                'data': []}
            for test_data in category_data['data']:
                test_result = {'title': test_data['title']}
                test_result['total_snp'] = len(test_data['snp'])
                test_result.update(self._check_snp(test_data['snp']))
                if test_result['snp'] and test_data.get('icon_result', False):
                    test_result['icon'] = test_data['icon_result'].get(
                        test_result['repute'], False)
                if test_result['snp'] and len(test_result['snp']) > 0:
                    result[category]['data'].append(test_result)
                elif test_data.get('default', False):
                    test_result['default'] = test_data['default']
                    test_result['repute'] = True
                    result[category]['data'].append(test_result)
                else:
                    test_result['default'] = '''
No hay resultados que cumplan los criterios.'''
                    test_result['repute'] = None
                    result[category]['data'].append(test_result)
            # if len(result[category]['data']) <= 0:
            #     del result[category]
        self.render({'result': result})
