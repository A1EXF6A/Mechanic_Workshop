from odoo import models, fields, api
import math

class MathOperation(models.Model):
    _name = "math.operation"
    _description = "Operaciones Matemáticas"

    name = fields.Char(
        string="Descripcion",
        compute="_compute_name",
        store=True
    )

    operand_1 = fields.Float(string="Operando 1", required=True)
    operand_2 = fields.Float(string="Operando 2", required=True)

    operation_type = fields.Selection([
        ('suma', "Suma"),
        ('resta', "Resta"),
        ('multiplicacion', "Multiplicación"),
        ('division', "División"),
        ('avg', "Promedio"),
        ('sqrt', "Raiz"),
        ('percent', "Porcentaje"),
        ('pow', "Potencia")
    ], required=True)

    result = fields.Float(
        string="Resultado",
        compute="_compute_result",
        store=True
    )

    operation_date = fields.Datetime(default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    notes = fields.Text()
    active = fields.Boolean(default=True)

    @api.depends("operand_1", "operand_2", "operation_type")
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.operation_type} ({rec.operand_1}, {rec.operand_2})"

    @api.depends("operand_1", "operand_2", "operation_type")
    def _compute_result(self):
        for rec in self:

            if rec.operation_type == "suma":
                rec.result = rec.operand_1 + rec.operand_2

            elif rec.operation_type == "resta":
                rec.result = rec.operand_1 - rec.operand_2

            elif rec.operation_type == "multiplicacion":
                rec.result = rec.operand_1 * rec.operand_2

            elif rec.operation_type == "division":
                rec.result = rec.operand_1 / rec.operand_2 if rec.operand_2 != 0 else 0

            elif rec.operation_type == "avg":
                rec.result = (rec.operand_1 + rec.operand_2) / 2

            elif rec.operation_type == "percent":
                rec.result = (rec.operand_1 * rec.operand_2) / 100

            elif rec.operation_type == "sqrt":
                rec.result = round(math.sqrt(rec.operand_1), 2)

            elif rec.operation_type == "pow":
                rec.result = rec.operand_1 ** rec.operand_2