    く__,.ヘヽ.　　　　/　,ー､ 〉
    　　　　　＼ ', !-─‐-i　/　/´
    　　　 　 ／｀ｰ'　　　 L/／｀ヽ､
    　　 　 /　 ／,　 /|　 ,　 ,　　　 ',
    　　　ｲ 　/ /-‐/　ｉ　L_ ﾊ ヽ!　 i
    　　　 ﾚ ﾍ 7ｲ｀ﾄ　 ﾚ'ｧ-ﾄ､!ハ|　 |
    　　　　 !,/7 '0'　　 ´0iソ| 　 |　　　
    　　　　 |.从"　　_　　 ,,,, / |./ 　 |
    　　　　 ﾚ'| i＞.､,,__　_,.イ / 　.i 　|
    　　　　　 ﾚ'| | / k_７_/ﾚ'ヽ,　ﾊ.　|
    　　　　　　 | |/i 〈|/　 i　,.ﾍ |　i　|
    　　　　　　.|/ /　ｉ： 　 ﾍ!　　＼　|
    　　　 　 　 kヽ>､ﾊ 　 _,.ﾍ､ 　 /､!
    　　　　　　 !'〈//｀Ｔ´', ＼ ｀'7'ｰr'
    　　　　　　 ﾚ'ヽL__|___i,___,ンﾚ|ノ
    　　　　　 　　　ﾄ-,/　|___./
    　　　　　 　　　'ｰ'　　!_,.:

## 一. DNS Elasticsearch数据处理 ##


### 1-1. DNS数据入库 ###
> 配置文件 : dns/conf/dns.conf  
> 代码目录 : dns/core/index  
> 运行入口 : dns/core/index/main.py  
> 注意事项 :  
>> a. 在main.py的main函数中，把entrance(para)函数的参数改为配置文件dns.conf在你机子上的绝对路径  
>> b. 每天的数据在一个独立的index中，例如名为dns20160626的index  
>> c. 每个index中有两个集合，它们是querydata集合 and dnsdata集合  
<br/>


### 注 : dns/web/这个目录到时候要放到web服务目录下，更换ip or port时要修改 : ###
> dns/web/controller/ipPrefixSearch.php中的$url字符串变量中的地址和端口  
> dns/web/controller/domainSuffixSearch.php中的$url字符串变量中的地址和端口  
> dns/web/controller/domainSubSearch.php中的$url字符串变量中的地址和端口  
<br/>


### 1-2. 根据域名后缀来查询 ###
> 代码文件1 : dns/web/model/elasticConn.php  
> 代码文件2 : dns/web/model/domainQuery.php  
> 代码文件3 : dns/web/controller/domainSuffixSearch.php  
> 入口文件1 : dns/web/controller/domainSuffixSearch.php ( 通过web服务 )  
<table>
    <tr>
        <td width="15%"><strong>查询方式</strong></td>
        <td width="20%"><strong>集合 & 字段</strong></td>
        <td width="20%"><strong>输入示例</strong></td>
        <td width="45%"><strong>注意</strong></td>
    </tr>
    <tr>
        <td width="15%">使用域名解析器</td>
        <td width="20%">querydata集合的question字段 or dnsdata集合的name字段</td>
        <td width="20%">fromid=0, size=5, domainSuffix="edu.cn", date="20160626", ismeta=1</td>
        <td width="45%">date表示你要查哪一天的数据，格式必须按照"20160603"的格式。ismeta=1表示查querydata集合，ismeta=0表示查询dnsdata集合。fromid表示你从哪一条数据开始查，一般一开始查的时候都是从0开始，比如返回的数据一共有5条，那么下一页可能还有数据，则再次查询同样的域名后缀，fromid取刚才返回的数据中pagingid字段最大的值。如果返回的数据不足5条，则说明下一页没有数据了。</td>
    </tr>
</table>
<br/>


### 1-3. 根据域名子串来查询 ###
> 代码文件1 : dns/web/model/elasticConn.php  
> 代码文件2 : dns/web/model/domainQuery.php  
> 代码文件3 : dns/web/controller/domainSubSearch.php  
> 入口文件 : dns/web/controller/domainSubSearch.php ( 通过web服务 )  
<table>
    <tr>
        <td width="15%"><strong>查询方式</strong></td>
        <td width="20%"><strong>集合 & 字段</strong></td>
        <td width="20%"><strong>输入示例</strong></td>
        <td width="45%"><strong>注意</strong></td>
    </tr>
    <tr>
        <td width="15%">根据域名的子串</td>
        <td width="20%">querydata集合的question字段 or dnsdata集合的name字段</td>
        <td width="20%">fromid=0, size=5, domainSub="seu.edu", date="20160603", "ismeta"=1</td>
        <td width="45%">domainSub表示查询的域名子串，其余参数含义和上述相同</td>
    </tr>
</table>
<br/>


### 1-4. 根据IP来查询 ###
> 代码文件1 : dns/web/model/elasticConn.php  
> 代码文件2 : dns/web/model/ipQuery.php  
> 代码文件3 : dns/web/controller/ipPrefixSearch.php  
> 入口文件 : dns/web/controller/ipPrefixSearch.php ( 通过web服务 )  
<table>
    <tr>
        <td width="15%"><strong>查询方式</strong></td>
        <td width="20%"><strong>集合 & 字段</strong></td>
        <td width="20%"><strong>输入示例</strong></td>
        <td width="45%"><strong>注意</strong></td>
    </tr>
    <tr>
        <td width="15%">根据IP的前缀</td>
        <td width="20%">metadata集合的srcip字段　or dstip字段</td>
        <td width="20%">fromid=0, size=5, ipPrefix="202.119.32", date="20160603", term="srcip"</td>
        <td width="45%">term取值为"srcip"或"dstip"。其余参数的用法同上面。</td>
    </tr>
</table>
<br/>



## 二. 数据日常运行 ##


### 2-1. 导出数据并压缩 ###
> 配置文件 : dns/conf/dns.conf  
<table>
    <tr>
        <td width="30%"><strong>代码文件</strong></td>
        <td width="30%"><strong>用途</strong></td>
        <td width="40%"><strong>用法</strong></td>
    </tr>
    <tr>
        <td width="30%">dns/core/backup/initBackup.py</td>
        <td width="30%">创建一个备份仓库并初始化配置</td>
        <td width="40%">python initBackup.py ( 配置项可以在配置文件中改 )</td>
    </tr>
    <tr>
        <td width="30%">export.py</td>
        <td width="30%">导出一个index到磁盘 -> [ 删除原来elk中的这个index ] -> [ 然后把导出后的文件压缩 ]</td>
        <td width="40%">python export.py -i arg1 -c arg2 -d arg3 (其中arg1是index的名称，arg2为true表示要压缩否则不压缩，arg3为true表示要删除elasticsearch中的index否则不删除)</td>
    </tr>
</table>
> 注意事项 :  
>> a. 在elasticsearch.yml配置文件中加入一行配置 path.repo: ["/data/dnsbackup"]，这个路径自己定  
>> b. 如果要删除哪个压缩的index，强烈建议不要手动敲命令去删，而是用clean.py脚本，因为clean.py能够帮你修改备份仓库的元信息  
<br/>


### 2-2. 恢复导入 ###
> 配置文件 : dns/conf/dns.conf  
<table>
    <tr>
        <td width="30%"><strong>代码文件</strong></td>
        <td width="30%"><strong>用途</strong></td>
        <td width="40%"><strong>用法</strong></td>
    </tr>
    <tr>
        <td width="30%">dns/core/backup/restore.py</td>
        <td width="30%">解压数据文件 -> 导入elasticsearch -> 删除原来的这份备份</td>
        <td width="40%">python restore.py arg1 ( arg1是你要恢复的index，例如 python restore.py dns20160626 )</td>
    </tr>
</table>
<br/>


### 2-3. 删除压缩数据 ###
> 配置文件 : dns/conf/dns.conf  
<table>
    <tr>
        <td width="30%"><strong>代码文件</strong></td>
        <td width="30%"><strong>用途</strong></td>
        <td width="40%"><strong>用法</strong></td>
    </tr>
    <tr>
        <td width="30%">dns/core/backup/clean.py</td>
        <td width="30%">删除压缩的数据文件 -> 修改备份仓库的元信息(即在备份仓库目录下的名为index的文件)</td>
        <td width="40%">python clean.py arg1 ( arg1是你要删除的索引的名字，例如 python clean.py dns20160626 )</td>
    </tr>
</table>
> 注意事项 :  
>> a. 如果要删除哪个压缩的index，强烈建议不要手动敲命令去删，而是用clean.py脚本，因为clean.py能够帮你修改备份仓库的元信息  
<br/>
