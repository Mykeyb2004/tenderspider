## 压缩数据库大小
是的，SQLite3 提供了一种叫做“压缩数据库”的操作，可以减小数据库文件的大小。具体的步骤如下：

1. 打开 SQLite3 命令行工具。

2. 连接到你要压缩的数据库：

```
sqlite3 database.db
```

- `database.db` 是要压缩的数据库文件名。

3. 在 SQLite3 命令行工具中输入以下命令：

```
VACUUM;
```

- `VACUUM` 命令会重新整理数据库文件，删除已经被标记为无效的数据行和空闲页，并且重新组织已有的数据页以使得数据库文件更加紧凑。

4. 当 `VACUUM` 命令执行完毕后，可以使用以下命令检查数据库文件的大小：

```
SELECT page_count * page_size AS size FROM pragma_page_count(), pragma_page_size();
```

- `page_count` 和 `page_size` 是 SQLite3 的系统表，用于记录数据库文件的页数和每页的字节数。
- `SELECT` 语句会将页数乘以每页的字节数以计算出数据库文件的大小，单位是字节。

需要注意的是，压缩数据库可能需要消耗一定的时间和计算资源，并且在某些情况下可能会降低数据库查询的性能。因此，建议在必要的时候才进行压缩操作，并充分测试数据库的性能和稳定性。


## 修改数据库结构
是的，在 SQLite3 中可以运行批量 SQL 语句，以一次性执行多个 SQL 命令。SQLite3 提供两种方式实现批量 SQL 语句：

1. 使用分号 `;` 分隔多个 SQL 语句：

在 SQLite3 的命令行工具中，可以使用分号 `;` 将多个 SQL 命令连接起来，以一次性执行这些命令。例如：

```
sqlite> SELECT * FROM mytable;
sqlite> INSERT INTO mytable (name, age) VALUES ('Jack', 25);
sqlite> UPDATE mytable SET age = 30 WHERE name = 'Jack';
```

这三个 SQL 命令之间用分号 `;` 相连，可以一次性执行。

2. 将 SQL 命令保存到文本文件中，并使用 `.read` 命令执行：

可以将多个 SQL 命令保存到一个文本文件中，每个 SQL 命令一行，然后在 SQLite3 的命令行工具中使用 `.read` 命令执行该文件。例如：

在 `mycommands.sql` 文件中保存了多个 SQL 命令：

```
SELECT * FROM mytable;
INSERT INTO mytable (name, age) VALUES ('Jack', 25);
UPDATE mytable SET age = 30 WHERE name = 'Jack';
```

在 SQLite3 的命令行工具中执行 `.read` 命令，指定 `mycommands.sql` 文件的路径即可执行多个 SQL 命令：

```
sqlite> .read mycommands.sql
```

需要注意的是，批量执行 SQL 命令可能会导致数据一次性修改多次，因此在生产环境中需要谨慎处理，以避免出现不必要的错误。

在 SQLite3 中进行完整性检查，可以使用以下两种命令：

1. PRAGMA integrity_check;

这个命令会检查数据库的所有表的完整性。如果数据库中任何一张表的行或索引存在问题，那么该命令会返回错误信息并且停止执行。

2. PRAGMA quick_check;

这个命令也会检查数据库的完整性，但是只检查表级别的结构和数据页的一致性。相对于 `integrity_check` 命令，它检查的内容更少，但是消耗的时间和计算资源也更少。

需要注意的是，完整性检查应该在定期维护数据库时进行，并且在备份、恢复、迁移等关键操作前进行检查以保证数据库稳定和可靠。如果发现了完整性问题，可以尝试使用 SQLite3 提供的修复工具或者手动修复数据库来解决问题。


## crontab(定时任务，已验证)
带参数版本：
```bash
50 * * * * /usr/bin/python3.8 /home/tender/tender_spider.py list >> /home/tender/output.log 2>&1
*/40 * * * * /usr/bin/python3.8 /home/tender/tender_spider.py detail >> /home/tender/output_detail.log 2>&1
```
上面第2条，表示每隔40分钟执行一次。


未带参数版本(废弃)：
```bash
35 * * * * /usr/bin/python3.8 /home/tender/tender_spider.py >> /home/tender/output.log 2>&1
```

## 进程守护启动命令（**未试验成功**）
```bash
pm2 start /home/tender/main.py --name "tender_list" --interpreter /usr/bin/python3.8 --watch
```
log所在目录
/home/ubuntu/.pm2/logs/



## 爬取详情页
```bash
/home/tender/venv/bin/python /home/tender/tender_detail.py
```

## 启动脚本
```bash
pm2 start /home/tender/main.py --name "tender_list" --interpreter /home/tender/venv/bin/python --watch
```
## 重启脚本
```bash
pm2 restart tender_list
```
## 停止脚本
```bash
pm2 stop tender_list
```
## 删除脚本
```bash
pm2 delete tender_list
```
## 查看日志
```bash
pm2 logs tender_list
```
## 查看脚本状态
```bash
pm2 status tender_list
```
## 查看所有脚本状态
```bash
pm2 status
```
## 查看脚本信息
```bash
pm2 info tender_list
```
## 查看所有脚本信息
```bash
pm2 info
```
## 查看脚本错误日志
```bash
pm2 show tender_list
```

---
`crontab` 命令是用来安装、查看和编辑用户的计划任务的，它可以让用户在指定时间和日期自动运行特定的命令和脚本。`crontab` 命令的常用参数如下：

- `-e`: 编辑当前用户的 crontab 文件；
- `-l`: 列出当前用户的所有计划任务；
- `-r`: 删除当前用户的所有计划任务；
- `-u user`: 指定要修改 crontab 文件的用户，如果不指定则默认为当前用户。

在编辑 crontab 文件时，有一些特殊的符号和关键字需要注意，它们的含义如下：

- `*`: 匹配任意值；
- `,`: 枚举多个值；
- `-`: 指定一个范围；
- `/`: 指定步长；
- `0-6`: 代表星期天到星期六；
- `@reboot`: 在系统启动时执行；
- `@hourly`: 每小时执行一次；
- `@daily` 或 `@midnight`: 每天凌晨执行一次；
- `@weekly`: 每周执行一次。

除了上述关键字和符号以外，cron 表达式还包括了五个时间字段，表示分、时、日、月和周几。这些字段需要使用数字来指定具体的时间或日期，例如 `0 0 * * *` 表示每天的 0 点 0 分执行。
