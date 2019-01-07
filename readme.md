## ``
该项目简单封装了mssql存储过程的几种调用方法
需配合microsoft 官方驱动odbc使用  
[microsoft官方文档](https://docs.microsoft.com/zh-cn/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017#troubleshooting-connection-problems)
简易安装参考
```    
    sudo su
    
    #Download appropriate package for the OS version
    #Choose only ONE of the following, corresponding to your OS version
    
    #RedHat Enterprise Server 6
    curl https://packages.microsoft.com/config/rhel/6/prod.repo > /etc/yum.repos.d/mssql-release.repo
    
    #RedHat Enterprise Server 7
    curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo
    
    exit
    sudo yum remove unixODBC-utf16 unixODBC-utf16-devel #to avoid conflicts
    sudo ACCEPT_EULA=Y yum install msodbcsql17
    # optional: for bcp and sqlcmd
    sudo ACCEPT_EULA=Y yum install mssql-tools
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
    source ~/.bashrc
    # optional: for unixODBC development headers
    sudo yum install unixODBC-devel
    
    
    # Prepare a temp file for defining the DSN to your database server
    vi /home/user/odbcadd.txt
    
    [MyMSSQLServer]
    Driver      = ODBC Driver 17 for SQL Server
    Description = My MS SQL Server
    Trace       = No
    Server      = 10.100.1.10
    
    # register the SQL Server database DSN information in /etc/odbc.ini
    sudo odbcinst -i -s -f /home/user/odbcadd.txt -l
    
    # check the DSN installation with:
    odbcinst -j
    cat /etc/odbc.ini
    
    # should contain a section called [MyMSSQLServer]
    
    # install the python driver for database connection
    pip install pyodbc
```
