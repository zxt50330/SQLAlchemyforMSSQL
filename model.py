# -*- coding: utf-8 -*-
# © 2018 QYT Technology
# Authored by: Zhao Xingtao (zxt50330@gmail.com)


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ModelBase(object):
    """
    需要定义database
    """
    database = ''

    @classmethod
    def call_procedure(cls, procedure_name, *args):
        """调用存储过程"""
        connection = db.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("use %s" % cls.database)
            params = ','.join(args)
            print(params)
            rows = cursor.execute("SET NOCOUNT ON; EXEC %s %s" % (procedure_name, params)).fetchall()
            col_name_list = [tuple[0] for tuple in cursor.description]
            cursor.close()
            connection.commit()
            return cls()._trans_data(col_name_list, rows)
        finally:
            connection.close()

    def _trans_data(self, col_name_list, rows):
        data_list = []
        for row in rows:
            assert len(row) == len(col_name_list)
            data_dict = {}
            for index, col_name in enumerate(col_name_list):
                data_dict.setdefault(col_name, row[index])
            data_list.append(data_dict)
        return data_list

    @classmethod
    def call_procedure_with_output(cls, procedure_name, *args, **kwargs):
        """
        有输出的储存过程 需要写明每个输入参数
        # FIXME: output默认为strErrorDescribe,没问题的话就不管了
        """
        params_str = ''
        for k, v in kwargs.items():

            k = '@' + k
            if isinstance(v, int):
                params_str += k + ' = ' + str(v) + ',\r\n'
            else:
                params_str += k + ' = N\'' + str(v) + '\',\r\n'
        sql = """\
        DECLARE @return_value int, @out nvarchar(max);
        EXEC @return_value = [dbo].[%s]\r\n %s @strErrorDescribe = @out OUTPUT
        SELECT @out AS the_output
        SELECT	'Return Value' = @return_value
        """ % (procedure_name, params_str)
        print(sql)
        connection = db.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SET NOCOUNT ON; use %s" % cls.database)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return_list = []
            while rows:
                col_name_list = [tuple[0] for tuple in cursor.description]
                return_list.append(cls()._trans_data(col_name_list, rows))
                if cursor.nextset():
                    rows = cursor.fetchall()
                else:
                    rows = None
            cursor.close()
            connection.commit()
            return return_list
        finally:
            connection.close()

    @classmethod
    def call_procedure_sql(cls, procedure_name, *args, **kwargs):
        """
        返回值
        """
        params_str = ''
        for k, v in kwargs.items():

            k = '@' + k
            if isinstance(v, int):
                params_str += k + ' = ' + str(v) + ',\r\n'
            else:
                if v:
                    params_str += k + ' = N\'' + str(v) + '\',\r\n'
                else:
                    params_str += k + ' = ' + 'NULL' + ',\r\n'
        sql = """\
        DECLARE @return_value int;
        EXEC @return_value = [dbo].[%s]\r\n %s
        SELECT	'Return Value' = @return_value
        """ % (procedure_name, params_str[:-3])
        print(sql)
        connection = db.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SET NOCOUNT ON; use %s" % cls.database)
            cursor.execute(sql)
            print(cursor.description)
            rows = cursor.fetchall()
            return_list = []
            while rows:
                col_name_list = [tuple[0] for tuple in cursor.description]
                return_list.append(cls()._trans_data(col_name_list, rows))
                if cursor.nextset():
                    rows = cursor.fetchall()
                else:
                    rows = None
            cursor.close()
            connection.commit()
            return return_list
        finally:
            connection.close()

    @classmethod
    def call_procedure_by_page(cls, table_name, PageSize, PageIndex, return_fields='*', where='', orderby='id'):
        """
        分页查询
        orderby: 'id desc'
        """
        order_by = 'ORDER BY %s' % orderby
        sql = """\
        DECLARE @return_value int, @PageCount int, @RecordCount int;
        EXEC @return_value = [dbo].[WEB_PageView]
        @TableName = N'%s',
        @ReturnFields = N'%s',
        @PageSize = %s,
        @PageIndex = %s,
        @Where = N'%s',
        @OrderBy = N'%s',
        @PageCount = @PageCount OUTPUT,
        @RecordCount = @RecordCount OUTPUT

        SELECT @PageCount AS PageCount,
               @RecordCount AS RecordCount

        SELECT	'Return Value' = @return_value

        """ % (table_name, return_fields, PageSize, PageIndex, where, order_by)
        print(sql)
        connection = db.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("use %s" % cls.database)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return_list = []
            while rows:
                col_name_list = [tuple[0] for tuple in cursor.description]
                return_list.append(cls()._trans_data(col_name_list, rows))
                if cursor.nextset():
                    rows = cursor.fetchall()
                else:
                    rows = None
            cursor.close()
            connection.commit()
            if return_list:
                return {
                    'data': return_list[0],
                    'page': return_list[1][0]
                }
            else:
                return {
                    'data': '',
                    'page': ''
                }
        finally:
            connection.close()