import pymysql
import random
import string
from datetime import datetime

# ---------------------- 配置项（修改为你的实际用户名/密码） ----------------------
MYSQL_CONFIG = {
    "host": "10.104.1.214",
    "port": 4306,
    "user": "tob_galaxy_order",  # 替换为你的MySQL用户名
    "password": "f5f1525aa60f2333",  # 替换为你的MySQL密码
    "database": "tob_galaxy_order",
    "charset": "utf8mb4"
}
TABLE_NAME = "TB_TOB_GALAXY_CHANNEL_ORDER"
TOTAL_ROWS = 200000  # 20万条数据
BATCH_SIZE = 1000  # 每批插入1000条（平衡效率和内存，可调整为500-2000）
FIXED_CREATOR_NAME = "批量导出组件测试"  # 固定标记，方便后续删除


# ---------------------- 工具函数：生成符合字段要求的随机数据 ----------------------
def generate_random_data():
    """生成单条符合表结构的随机数据"""

    # 生成随机字符串（用于订单号等字段）
    def random_str(length=32):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # 当前时间戳（毫秒级，匹配bigint字段）
    current_ts = int(datetime.now().timestamp() * 1000)
    # 随机时间戳（略早于当前时间，模拟历史订单）
    random_ts = current_ts - random.randint(0, 3600 * 24 * 7 * 1000)  # 7天内随机

    # 构造单条数据（严格匹配表结构，满足非空/默认值约束）
    return (
        random.randint(1, 100),  # channelId（1-100随机渠道）
        random_str(64),  # channelOrderId（唯一订单号，避免重复）
        random_str(64),  # originOrderId
        random_ts,  # submitTime（下单时间）
        random_ts if random.choice([True, False]) else 0,  # payTime（部分订单有支付时间）
        round(random.uniform(0.01, 9999.99), 2),  # realPrice（实付金额，保留2位小数）
        round(random.uniform(0, 99.99), 2),  # expFee（邮费）
        random.choice([1, 2]),  # type（1:普通订单；2:集采订单）
        random.choice([1, 2]),  # submitType（1:普通下单；2:预占下单）
        random.choice([1, 2, 3, 4, 6]),  # status（避开5:取消待确认、7:下单失败，减少异常）
        random.randint(1, 10),  # orderSource（1-10随机来源）
        json.dumps({"test": "batch_data", "order_no": random_str(16)}),  # extInfo（JSON格式额外信息）
        "",  # failInfo（无失败，留空）
        random_str(32),  # creator（创建人uid）
        FIXED_CREATOR_NAME,  # creatorName（固定标记，核心需求）
        current_ts,  # createTime（创建时间）
        current_ts,  # updateTime（更新时间）
        random.choice([0, 1]),  # retryFlag（卡单重推标志）
        random.choice([0, 24, 48, 72, -1]),  # overtimeType（超时类型）
        0,  # deliveryOverTime（无超时妥投，留0）
        round(random.uniform(0, 9999.99), 2),  # companyPayPrice（企业支付金额）
        round(random.uniform(0, 9999.99), 2),  # personalPayPrice（个人支付金额）
        random.randint(0, 1000),  # submitDistributorId（提交服务商ID）
        random.randint(0, 1000),  # distributorId（分发服务商ID）
        random_str(64)  # projectId（项目ID）
    )


# ---------------------- 核心流程：连接验证 + 批量插入 ----------------------
def main():
    conn = None
    cursor = None
    try:
        # 1. 建立MySQL连接（验证连接是否成功）
        print("正在验证MySQL连接...")
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        print("✅ MySQL连接成功！")

        # 2. 定义插入SQL（id是自增主键，无需传入；字段顺序严格匹配表结构）
        insert_sql = f"""
        INSERT INTO {TABLE_NAME} (
            channelId, channelOrderId, originOrderId, submitTime, payTime,
            realPrice, expFee, type, submitType, status,
            orderSource, extInfo, failInfo, creator, creatorName,
            createTime, updateTime, retryFlag, overtimeType, deliveryOverTime,
            companyPayPrice, personalPayPrice, submitDistributorId, distributorId, projectId
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        """

        # 3. 批量生成并插入数据（分批次提交，提升效率）
        print(f"开始插入 {TOTAL_ROWS} 条数据，每批插入 {BATCH_SIZE} 条...")
        total_inserted = 0
        batch_data = []

        for i in range(TOTAL_ROWS):
            # 生成单条数据并加入批量列表
            single_data = generate_random_data()
            batch_data.append(single_data)

            # 每积累BATCH_SIZE条，执行一次批量插入
            if len(batch_data) >= BATCH_SIZE:
                cursor.executemany(insert_sql, batch_data)
                conn.commit()  # 提交事务
                total_inserted += len(batch_data)
                batch_data.clear()  # 清空批量列表

                # 打印进度
                print(f"已插入 {total_inserted}/{TOTAL_ROWS} 条数据")

        # 4. 插入剩余不足一批的数据
        if batch_data:
            cursor.executemany(insert_sql, batch_data)
            conn.commit()
            total_inserted += len(batch_data)

        print(f"\n✅ 数据插入完成！共成功插入 {total_inserted} 条数据")
        print(f"🔍 标记字段 creatorName = '{FIXED_CREATOR_NAME}'，后续可通过该字段删除脏数据")

    except pymysql.Error as e:
        # 数据库错误回滚事务
        if conn:
            conn.rollback()
        print(f"❌ MySQL操作异常：{e}")
    except Exception as e:
        print(f"❌ 程序运行异常：{str(e)}")
    finally:
        # 5. 关闭游标和连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("✅ MySQL连接已关闭")


# ---------------------- 后续删除脏数据的SQL（备用） ----------------------
def get_delete_sql():
    """返回删除本次批量插入脏数据的SQL（测试完成后执行）"""
    return f"""
    DELETE FROM {TABLE_NAME} WHERE creatorName = '{FIXED_CREATOR_NAME}';
    """


if __name__ == "__main__":
    print("正在验证MySQL连接...")
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    print("✅ MySQL连接成功！")