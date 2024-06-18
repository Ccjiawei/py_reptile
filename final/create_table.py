import mysql.connector

# 连接到数据库
conn = mysql.connector.connect(host='81.68.197.104', user='root', password='Baiwa@0601', port=3307,  database='python_test_202404')
cursor = conn.cursor()

# 定义要创建的表名列表
table_names = ['ae_stock_info','ar_stock_info','at_stock_info','au_stock_info','ba_stock_info','bd_stock_info','be_stock_info','bg_stock_info','bh_stock_info','br_stock_info','bw_stock_info','ca_stock_info','ch_stock_info','ci_stock_info','cl_stock_info','cn_stock_info','co_stock_info','cr_stock_info','cy_stock_info','cz_stock_info','de_stock_info','dk_stock_info','ee_stock_info','eg_stock_info','es_stock_info','fi_stock_info','fr_stock_info','gr_stock_info','hr_stock_info','hu_stock_info','id_stock_info','ie_stock_info','il_stock_info','ind_stock_info','iq_stock_info','is_stock_info','it_stock_info','jm_stock_info','jo_stock_info','jp_stock_info','ke_stock_info','kr_stock_info','kw_stock_info','kz_stock_info','lb_stock_info','lk_stock_info','lt_stock_info','lu_stock_info','lv_stock_info','ma_stock_info','me_stock_info','mn_stock_info','mt_stock_info','mu_stock_info','mw_stock_info','mx_stock_info','my_stock_info','na_stock_info','ng_stock_info','nl_stock_info','no_stock_info','nor_stock_info','nz_stock_info','om_stock_info','pe_stock_info','ph_stock_info','pk_stock_info','pl_stock_info','ps_stock_info','pt_stock_info','qa_stock_info','ro_stock_info','rs_stock_info','ru_stock_info','rw_stock_info','sa_stock_info','se_stock_info','sg_stock_info','si_stock_info','sk_stock_info','th_stock_info','tn_stock_info','tr_stock_info','tw_stock_info','tz_stock_info','ua_stock_info','ug_stock_info','uk_stock_info','us_stock_info','ve_stock_info','vn_stock_info','za_stock_info','zm_stock_info','zw_stock_info']

for table in table_names:
    # 构造CREATE TABLE语句
    create_query = f"CREATE TABLE {table} (`id` int(11) NOT NULL AUTO_INCREMENT," \
                   f" `stock_code` varchar(255) DEFAULT NULL COMMENT '股票代码'," \
                   f" `currency` varchar(255) DEFAULT NULL COMMENT '货币'," \
                   f" `exchange_name` varchar(255) DEFAULT NULL COMMENT '交易所名称'," \
                   f" `block_item_name` varchar(255) DEFAULT NULL COMMENT '指标所属板块名称'," \
                   f" `item_name` varchar(255) DEFAULT NULL COMMENT '指标名称'," \
                   f" `item_value` varchar(255) DEFAULT NULL COMMENT '指标值'," \
                   f" `item_date` varchar(255) DEFAULT NULL COMMENT '指标日期'," \
                   f" `item_year` varchar(255) DEFAULT NULL COMMENT '年度'," \
                   f" PRIMARY KEY (`id`)," \
                   f" UNIQUE KEY check_repeat_key (stock_code, block_item_name, item_name, item_year))"

    try:
        cursor.execute(create_query)
        print(f'成功创建表{table}')

    except Exception as e:
        print(f'创建表{table}时发生错误：{e}')

# 关闭数据库连接
cursor.close()
conn.close()