from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, AccessError
from odoo import fields
from datetime import datetime, timedelta


class TestTechStoreTechnician(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Client',
            'email': 'test@example.com',
        })
        self.Partner = self.env['res.partner']
        self.Technician = self.env['techstore.technician']
        self.Equipment = self.env['techstore.equipment']
        self.Maintenance = self.env['techstore.maintenance']
        self.Metrics = self.env['techstore.maintenance.metrics']
        self.History = self.env['techstore.maintenance.history']

    def _create_technician(self, **kwargs):
        vals = {
            'name': 'Test Technician',
            'identification': '12345',
            'phone': '+15551234567',
            'email': 'tech@test.com',
            'specialty': 'hardware',
        }
        vals.update(kwargs)
        return self.Technician.create(vals)

    def _create_equipment(self, **kwargs):
        vals = {
            'partner_id': self.partner.id,
            'equipment_type': 'laptop',
            'brand': 'TestBrand',
            'model': 'TestModel',
            'serial_number': 'SN-TEST-001',
        }
        vals.update(kwargs)
        return self.Equipment.create(vals)

    def _create_maintenance(self, **kwargs):
        vals = {
            'partner_id': self.partner.id,
            'equipment_id': self._create_equipment().id,
            'description': 'Test issue',
        }
        vals.update(kwargs)
        return self.Maintenance.create(vals)

    # ────────── Technician Tests ──────────

    def test_technician_create(self):
        tech = self._create_technician()
        self.assertEqual(tech.name, 'Test Technician')
        self.assertEqual(tech.identification, '12345')
        self.assertEqual(tech.phone, '+15551234567')
        self.assertEqual(tech.email, 'tech@test.com')
        self.assertEqual(tech.specialty, 'hardware')
        self.assertTrue(tech.active)
        self.assertEqual(tech.maintenance_count, 0)
        self.assertEqual(tech.workload_level, 'low')

    def test_technician_duplicate_identification(self):
        self._create_technician(identification='DUP123')
        with self.assertRaises(ValidationError):
            self._create_technician(identification='DUP123')

    def test_technician_invalid_email(self):
        with self.assertRaises(ValidationError):
            self._create_technician(email='not-an-email')

    def test_technician_empty_phone(self):
        with self.assertRaises(ValidationError):
            self._create_technician(phone='')

    def test_technician_maintenance_count(self):
        tech = self._create_technician()
        equip = self._create_equipment()
        self.Maintenance.create({
            'partner_id': self.partner.id,
            'equipment_id': equip.id,
            'technician_id': tech.id,
            'description': 'Maint 1',
            'state': 'en_proceso',
        })
        self.Maintenance.create({
            'partner_id': self.partner.id,
            'equipment_id': equip.id,
            'technician_id': tech.id,
            'description': 'Maint 2',
            'state': 'nuevo',
        })
        self.Maintenance.create({
            'partner_id': self.partner.id,
            'equipment_id': equip.id,
            'technician_id': tech.id,
            'description': 'Maint 3',
            'state': 'finalizado',
        })
        self.Maintenance.create({
            'partner_id': self.partner.id,
            'equipment_id': equip.id,
            'technician_id': tech.id,
            'description': 'Maint 4',
            'state': 'cancelado',
        })
        self.assertEqual(tech.maintenance_count, 2)

    def test_technician_workload_level_low(self):
        tech = self._create_technician()
        self.assertLessEqual(tech.maintenance_count, 2)
        self.assertEqual(tech.workload_level, 'low')

    def test_technician_workload_level_medium(self):
        tech = self._create_technician()
        equip = self._create_equipment()
        for i in range(4):
            self.Maintenance.create({
                'partner_id': self.partner.id,
                'equipment_id': equip.id,
                'technician_id': tech.id,
                'description': f'Maint {i}',
                'state': 'en_proceso',
            })
        self.assertIn(tech.maintenance_count, range(3, 6))
        self.assertEqual(tech.workload_level, 'medium')

    def test_technician_workload_level_high(self):
        tech = self._create_technician()
        equip = self._create_equipment()
        for i in range(7):
            self.Maintenance.create({
                'partner_id': self.partner.id,
                'equipment_id': equip.id,
                'technician_id': tech.id,
                'description': f'Maint {i}',
                'state': 'en_proceso',
            })
        self.assertIn(tech.maintenance_count, range(6, 9))
        self.assertEqual(tech.workload_level, 'high')

    def test_technician_workload_level_critical(self):
        tech = self._create_technician()
        equip = self._create_equipment()
        for i in range(10):
            self.Maintenance.create({
                'partner_id': self.partner.id,
                'equipment_id': equip.id,
                'technician_id': tech.id,
                'description': f'Maint {i}',
                'state': 'en_proceso',
            })
        self.assertGreater(tech.maintenance_count, 8)
        self.assertEqual(tech.workload_level, 'critical')

    # ────────── Equipment Tests ──────────

    def test_equipment_create(self):
        equip = self._create_equipment()
        self.assertTrue(equip.code)
        self.assertNotEqual(equip.code, 'New')
        self.assertEqual(equip.partner_id, self.partner)
        self.assertEqual(equip.equipment_type, 'laptop')
        self.assertEqual(equip.serial_number, 'SN-TEST-001')
        self.assertEqual(equip.state, 'received')

    def test_equipment_code_sequence(self):
        equip = self._create_equipment()
        self.assertTrue(equip.code.startswith('EQUIP/'))

    def test_equipment_duplicate_serial(self):
        self._create_equipment(serial_number='SN-DUP')
        with self.assertRaises(ValidationError):
            self._create_equipment(serial_number='SN-DUP')

    def test_equipment_state_transitions(self):
        equip = self._create_equipment()
        self.assertEqual(equip.state, 'received')
        equip.state = 'under_repair'
        self.assertEqual(equip.state, 'under_repair')
        equip.state = 'repaired'
        self.assertEqual(equip.state, 'repaired')
        equip.state = 'delivered'
        self.assertEqual(equip.state, 'delivered')

    # ────────── Maintenance Tests ──────────

    def test_maintenance_create(self):
        maint = self._create_maintenance()
        self.assertTrue(maint.number)
        self.assertNotEqual(maint.number, 'New')
        self.assertEqual(maint.state, 'nuevo')
        self.assertEqual(len(maint.history_ids), 1)
        self.assertEqual(maint.history_ids[0].new_state, 'nuevo')
        metrics = self.Metrics.search([('maintenance_id', '=', maint.id)])
        self.assertEqual(len(metrics), 1)

    def test_maintenance_number_sequence(self):
        maint = self._create_maintenance()
        self.assertTrue(maint.number.startswith('MAINT/'))

    def test_maintenance_state_flow_new_to_finalized(self):
        maint = self._create_maintenance()
        self.assertEqual(maint.state, 'nuevo')

        maint.state = 'asignado'
        self.assertEqual(maint.state, 'asignado')

        maint.state = 'en_proceso'
        self.assertEqual(maint.state, 'en_proceso')

        maint.state = 'pendiente'
        self.assertEqual(maint.state, 'pendiente')

        maint.state = 'finalizado'
        self.assertEqual(maint.state, 'finalizado')

    def test_maintenance_state_cancel(self):
        maint = self._create_maintenance()
        maint.state = 'cancelado'
        self.assertEqual(maint.state, 'cancelado')

    def test_maintenance_auto_start_date(self):
        maint = self._create_maintenance()
        self.assertFalse(maint.start_date)
        maint.state = 'en_proceso'
        self.assertIsNotNone(maint.start_date)

    def test_maintenance_auto_end_date(self):
        maint = self._create_maintenance()
        maint.state = 'en_proceso'
        maint.state = 'finalizado'
        self.assertIsNotNone(maint.end_date)

    def test_maintenance_history_on_state_change(self):
        maint = self._create_maintenance()
        initial_count = len(maint.history_ids)
        maint.state = 'asignado'
        maint.state = 'en_proceso'
        maint.state = 'finalizado'
        self.assertEqual(len(maint.history_ids), initial_count + 3)

    def test_maintenance_history_content(self):
        maint = self._create_maintenance()
        maint.state = 'asignado'
        history = maint.history_ids[0]
        self.assertEqual(history.old_state, 'nuevo')
        self.assertEqual(history.new_state, 'asignado')
        self.assertEqual(history.user_id, self.env.user)

    def test_maintenance_real_time_computation(self):
        maint = self._create_maintenance()
        now = datetime.now()
        maint.write({
            'start_date': now - timedelta(hours=5),
            'end_date': now,
        })
        self.assertAlmostEqual(maint.real_time, 5.0, places=1)

    def test_maintenance_critical_priority_warning(self):
        rec = self.env['techstore.maintenance'].new({'priority': '3'})
        result = rec._onchange_priority()
        self.assertIn('warning', result)
        self.assertIn('Critical', result['warning']['title'])

    def test_maintenance_estimated_fields(self):
        maint = self._create_maintenance(
            estimated_cost=150.0,
            final_cost=200.0,
            estimated_time=4.0,
        )
        self.assertEqual(maint.estimated_cost, 150.0)
        self.assertEqual(maint.final_cost, 200.0)
        self.assertEqual(maint.estimated_time, 4.0)

    def test_maintenance_cascade_delete(self):
        maint = self._create_maintenance()
        maint_id = maint.id
        history_ids = maint.history_ids.ids
        metrics = self.Metrics.search([('maintenance_id', '=', maint_id)])
        self.assertTrue(metrics)
        metrics_id = metrics.id
        maint.unlink()
        self.assertFalse(self.Maintenance.browse(maint_id).exists())
        self.assertFalse(self.History.browse(history_ids).exists())
        self.assertFalse(self.Metrics.browse(metrics_id).exists())

    # ────────── Metrics Tests ──────────

    def test_metrics_auto_creation(self):
        maint = self._create_maintenance()
        metrics = self.Metrics.search([('maintenance_id', '=', maint.id)])
        self.assertEqual(len(metrics), 1)

    def test_metrics_attention_time(self):
        now = fields.Datetime.now()
        start = now + timedelta(hours=2)
        maint = self._create_maintenance()
        maint.write({
            'request_date': now,
            'start_date': start,
        })
        metrics = self.Metrics.search([('maintenance_id', '=', maint.id)])
        self.assertAlmostEqual(metrics.attention_time, 2.0, places=1)

    def test_metrics_sla_compliance_ok(self):
        now = fields.Datetime.now()
        maint = self._create_maintenance(
            estimated_time=5.0,
            start_date=now - timedelta(hours=3),
            end_date=now,
        )
        self.assertTrue(maint.real_time <= maint.estimated_time)
        metrics = self.Metrics.search([('maintenance_id', '=', maint.id)])
        self.assertTrue(metrics.sla_compliance)
        self.assertEqual(metrics.delay, 0.0)

    def test_metrics_sla_breach(self):
        now = fields.Datetime.now()
        maint = self._create_maintenance(
            estimated_time=2.0,
            start_date=now - timedelta(hours=5),
            end_date=now,
        )
        self.assertTrue(maint.real_time > maint.estimated_time)
        metrics = self.Metrics.search([('maintenance_id', '=', maint.id)])
        self.assertFalse(metrics.sla_compliance)
        self.assertGreater(metrics.delay, 0.0)

    def test_metrics_technician_efficiency(self):
        now = fields.Datetime.now()
        maint = self._create_maintenance(
            estimated_time=10.0,
            start_date=now - timedelta(hours=5),
            end_date=now,
        )
        metrics = self.Metrics.search([('maintenance_id', '=', maint.id)])
        expected = (maint.estimated_time / maint.real_time) * 100
        self.assertAlmostEqual(metrics.technician_efficiency, expected, places=1)

    def test_metrics_quality_indicator(self):
        maint = self._create_maintenance(customer_satisfaction='4')
        metrics = self.Metrics.search([('maintenance_id', '=', maint.id)])
        self.assertAlmostEqual(metrics.quality_indicator, 100.0)

        maint2 = self._create_maintenance(customer_satisfaction='1')
        metrics2 = self.Metrics.search([('maintenance_id', '=', maint2.id)])
        self.assertAlmostEqual(metrics2.quality_indicator, 25.0)

    def test_metrics_state_changes_count(self):
        maint = self._create_maintenance()
        maint.state = 'asignado'
        maint.state = 'en_proceso'
        maint.state = 'finalizado'
        metrics = self.Metrics.search([('maintenance_id', '=', maint.id)])
        self.assertEqual(metrics.state_changes_count, 4)

    # ────────── History Tests ──────────

    def test_history_order(self):
        maint = self._create_maintenance()
        maint.state = 'asignado'
        maint.state = 'en_proceso'
        records = maint.history_ids
        for i in range(len(records) - 1):
            self.assertGreaterEqual(
                records[i].change_date,
                records[i + 1].change_date,
            )

    # ────────── Security Tests ──────────

    def _create_user(self, group_xml_id):
        group = self.env.ref(group_xml_id)
        return self.env['res.users'].create({
            'name': 'Test User',
            'login': f'test_{group_xml_id.split(".")[-1]}@test.com',
            'groups_id': [(4, group.id)],
        })

    def test_security_technician_read_own(self):
        tech_user = self._create_user('techstore_maintenance.group_techstore_technician')
        partner_b = self.Partner.create({'name': 'Client B'})
        equip = self._create_equipment()
        equip_b = self._create_equipment(partner_id=partner_b.id, serial_number='SN-TEST-OWN')

        tech = self._create_technician(user_id=tech_user.id)
        maint_own = self._create_maintenance(technician_id=tech.id)
        maint_other = self.Maintenance.create({
            'partner_id': partner_b.id,
            'equipment_id': equip_b.id,
            'description': 'Other tech maintenance',
        })

        env_tech = self.env(user=tech_user)
        maint_ids = env_tech['techstore.maintenance'].search([])
        self.assertIn(maint_own, maint_ids)
        self.assertNotIn(maint_other, maint_ids)

    def test_security_technician_no_unlink(self):
        tech_user = self._create_user('techstore_maintenance.group_techstore_technician')
        tech = self._create_technician(user_id=tech_user.id)
        maint = self._create_maintenance(technician_id=tech.id)
        env_tech = self.env(user=tech_user)
        with self.assertRaises(AccessError):
            env_tech['techstore.maintenance'].browse(maint.id).unlink()

    def test_security_supervisor_read_all(self):
        sup_user = self._create_user('techstore_maintenance.group_techstore_supervisor')
        partner_b = self.Partner.create({'name': 'Client B'})
        equip = self._create_equipment()
        equip_b = self._create_equipment(partner_id=partner_b.id, serial_number='SN-SUP-TEST')

        tech = self._create_technician()
        maint_a = self._create_maintenance(technician_id=tech.id)
        maint_b = self.Maintenance.create({
            'partner_id': partner_b.id,
            'equipment_id': equip_b.id,
            'description': 'Supervisor sees this too',
        })

        env_sup = self.env(user=sup_user)
        maint_ids = env_sup['techstore.maintenance'].search([])
        self.assertIn(maint_a, maint_ids)
        self.assertIn(maint_b, maint_ids)

    def test_security_supervisor_no_unlink(self):
        sup_user = self._create_user('techstore_maintenance.group_techstore_supervisor')
        maint = self._create_maintenance()
        env_sup = self.env(user=sup_user)
        with self.assertRaises(AccessError):
            env_sup['techstore.maintenance'].browse(maint.id).unlink()

    def test_security_admin_full_access(self):
        admin_user = self._create_user('techstore_maintenance.group_techstore_admin')
        env_admin = self.env(user=admin_user)
        maint = self._create_maintenance()
        maint_admin = env_admin['techstore.maintenance'].browse(maint.id)
        self.assertTrue(maint_admin.exists())
        maint_admin.write({'description': 'Updated by admin'})
        self.assertEqual(maint_admin.description, 'Updated by admin')

    def test_security_technician_no_create_technician(self):
        tech_user = self._create_user('techstore_maintenance.group_techstore_technician')
        env_tech = self.env(user=tech_user)
        with self.assertRaises(AccessError):
            env_tech['techstore.technician'].create({
                'name': 'Unauthorized',
                'identification': 'NO',
                'phone': '+1',
            })

    def test_security_technician_equipment_read(self):
        tech_user = self._create_user('techstore_maintenance.group_techstore_technician')
        equip = self._create_equipment()
        env_tech = self.env(user=tech_user)
        equip_read = env_tech['techstore.equipment'].browse(equip.id)
        self.assertTrue(equip_read.exists())
