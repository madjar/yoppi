# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'File.old'
        db.delete_column('ftp_file', 'old')

    def backwards(self, orm):
        # Adding field 'File.old'
        db.add_column('ftp_file', 'old',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    models = {
        'ftp.file': {
            'Meta': {'object_name': 'File'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_directory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['ftp.FtpServer']"}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        'ftp.ftpserver': {
            'Meta': {'object_name': 'FtpServer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'indexing': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'last_online': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 9, 0, 0)'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['ftp']