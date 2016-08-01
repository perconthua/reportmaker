# -*- coding: utf-8 -*-

from __future__ import absolute_import
import __builtin__
import os
import datetime
import falcon
import json
import jinja2
import xlsxwriter
from reportmaker.libs.sql import *
from reportmaker.controllers.hooks import deserialize

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))),
    autoescape=True )

class report(object):
    def on_get(self, req, res):
        template=jinja_env.get_template("templates/index.html")

        res.content_type = 'text/html'
        res.status = falcon.HTTP_200
        res.body=template.render({"name":"report"})

    @falcon.before(deserialize)
    def on_post(self, req, res):
        try:
            query=req.params['body']['query']
            title=req.params['body']['title']
            
            self.create_report_from_query(title,query)
            
            res.status = falcon.HTTP_200
            res.body='{"message":"Report was created"}'
        except Exception, e:
            res.status = falcon.HTTP_400
            data={"message":"Query Error%s"%e}
            res.body=json.dumps(data)

    def create_report_from_query(self,title,query):
        try:
            db=connect()
            data= sql(db,query)
        except Exception, e:
            raise e    
            return

        self.create_file(title,data,query)
    
    def setWidth(self,index,data,lengths):
        if isinstance(data,unicode):
            length=len(str(data.encode('utf8')))
        else:
            length=len(str(data))

        if index in lengths:
            lengths[index] = max(lengths[index],length)
        else:
            lengths[index] = length

        lengths[index] = min(lengths[index],100)

    def create_file(self,title,data,query):
        filename = title.replace(" ","_").lower()
        workbook = xlsxwriter.Workbook(filename+'.xlsx')
        worksheet = workbook.add_worksheet('reporte')

        ftitle = workbook.add_format({'font_size':24})

        fheader = workbook.add_format({
             'bold': True,
             'font_color': 'white',
             'bg_color':'gray',
             'border' : 1
             })

        fborder = workbook.add_format({'border' : 1})
        fborderdate = workbook.add_format({'border' : 1, 'num_format': 'yyyy-mm-dd'})

        frow=2
        fcol=1
        worksheet.write(0,1,title,ftitle)
        lengths = {}
        if len(data)>0:
            worksheet.set_row(0,40)
            worksheet.write(frow,0,"",fheader)
            for col in data[0]:
                worksheet.write(frow,fcol,col,fheader)
                self.setWidth(fcol,col,lengths)
                fcol+=1


            frow+=1
            i=1
            
            for row in data:
                worksheet.write(frow,0,i,fborder)
                i+=1
                fcol=1
                for col in row:
                    if isinstance(row[col],datetime.datetime) or isinstance(row[col],datetime.date):
                        worksheet.write_datetime(frow,fcol,row[col],fborderdate)
                    else:
                        worksheet.write(frow,fcol,row[col],fborder)

                    self.setWidth(fcol,row[col],lengths)
                        
                    fcol+=1
                frow+=1

        for col in lengths:
            worksheet.set_column(col, col, lengths[col])

        worksheet2 = workbook.add_worksheet('query')
        query_lines = query.splitlines()
        i=0
        for line in query_lines:
            worksheet2.write(i,0,line)
            i+=1

        workbook.close()
