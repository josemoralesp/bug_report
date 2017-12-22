# -*- coding: utf-8 -*-
from odoo import api, models, fields


class BugReportLine(models.Model):
    _name = 'bug.report.line'

    bug_id = fields.Many2one('bug.report', 'Bug')
    ctrig = fields.Float('Trig', readonly=True)
    name = fields.Char()


class BugReport(models.Model):
    _name = 'bug.report'
    # _inherit = ['mail.thread']

    name = fields.Char()
    line_ids = fields.One2many('bug.report.line', 'bug_id', 'Lines')
    trig = fields.Integer()
    trig_total = fields.Float(compute='_compute_trig_total')

    @api.depends('trig')
    def _compute_trig_total(self):
        for record in self:
            lines = []
            total = 0
            for line in record.line_ids:
                ltotal = (record.trig * 2) + line.id
                total += ltotal
                lines += [
                    (1, line.id, {'ctrig': ltotal})]
            record.write({
                'line_ids': lines,
                'trig_total': total
            })
