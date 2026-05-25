move = env['account.move'].search([('move_type', '=', 'out_invoice')], limit=1, order='id desc')
print("Invoice:", move.name)
print("Untaxed:", move.amount_untaxed, "Tax:", move.amount_tax, "Total:", move.amount_total)
for line in move.invoice_line_ids:
    if line.display_type not in ('line_section', 'line_note'):
        taxes = line.tax_ids
        print(f"Line {line.name}: Subtotal={line.price_subtotal} Taxes={[t.amount for t in taxes]}")
