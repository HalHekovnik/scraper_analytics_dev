# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Worker'
        db.create_table('workers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'analytics', ['Worker'])

        # Adding model 'Reports'
        db.create_table('reports', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analytics.Worker'], db_column='worker')),
            ('time', self.gf('django.db.models.fields.FloatField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'analytics', ['Reports'])

        # Adding model 'Lessons'
        db.create_table('lessons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['analytics.Worker'], db_column='worker')),
            ('lesson', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'analytics', ['Lessons'])


    def backwards(self, orm):
        # Deleting model 'Worker'
        db.delete_table('workers')

        # Deleting model 'Reports'
        db.delete_table('reports')

        # Deleting model 'Lessons'
        db.delete_table('lessons')


    models = {
        u'analytics.lessons': {
            'Meta': {'object_name': 'Lessons', 'db_table': "'lessons'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analytics.Worker']", 'db_column': "'worker'"})
        },
        u'analytics.reports': {
            'Meta': {'object_name': 'Reports', 'db_table': "'reports'"},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'time': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['analytics.Worker']", 'db_column': "'worker'"})
        },
        u'analytics.worker': {
            'Meta': {'object_name': 'Worker', 'db_table': "'workers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['analytics']