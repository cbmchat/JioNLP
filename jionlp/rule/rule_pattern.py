# -*- coding=utf-8 -*-
# library: jionlp
# author: dongrixinyu
# license: Apache License 2.0
# Email: dongrixinyu.89@163.com
# github: https://github.com/dongrixinyu/JioNLP
# description: Preprocessing tool for Chinese NLP


from jionlp.util.funcs import absence


# ---------------------------------------------------------------------
# 手机号码
CELL_PHONE_PATTERN = r'(?<=[^\d])(((\+86)?([- ])?)?((1[3-9][0-9]))([- ])?\d{4}([- ])?\d{4})(?=[^\d])'
# 该规则用于抽取与判定手机号的归属地，即抽取前三位、中间4位
CELL_PHONE_CHECK_PATTERN = r'((1[3-9][0-9]))([- ])?\d{4}([- ])?\d{4}'

# ---------------------------------------------------------------------
# 中文字符正则
ANCIENT_CHINESE_CHAR_PATTERN = '[一-龥㐀-䶵]'  # 在 gb13000.1 基础上扩展 6582 个古汉字，共 27484 个汉字
# gb13000.1 收录的汉字 20902 个，但其中有很多不常用字，在 chinese_char_dictionary_loader 有说明
CHINESE_CHAR_PATTERN = '[一-龥]'

# ---------------------------------------------------------------------
# 国内固定电话号码
LANDLINE_PHONE_PATTERN = r'(?<=[^\d])(([\(（])?0\d{2,3}[\)） —-]{1,2}\d{7,8}|\d{3,4}[ -]\d{3,4}[ -]\d{4})(?=[^\d])'
LANDLINE_PHONE_CHECK_PATTERN = r'(([\(（])?0\d{2,3}[\)） —-]{1,2}\d{7,8}|\d{3,4}[ -]\d{3,4}[ -]\d{4})'
# 用分隔符，找到靠前的区号
LANDLINE_PHONE_AREA_CODE_PATTERN = r'(0\d{2,3})[\)） —-]'

# ---------------------------------------------------------------------
# 电子邮箱
# 邮箱中，允许中文等字符存在。但是，中文字符、#、* 会对结果造成较大干扰故忽略
EMAIL_PATTERN = r'(?<=[^0-9a-zA-Z.\-])' \
                r'([a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+(?:\.[a-zA-Z0-9_.-]+)*\.[a-zA-Z0-9]{2,6})' \
                r'(?=[^0-9a-zA-Z.\-])'
# 抽取邮箱的域名
EMAIL_DOMAIN_PATTERN = r'(?<=@)([0-9a-zA-Z]+)(?=\.)'

# ---------------------------------------------------------------------
# 转义符号
ESCAPE_CHAR_PATTERN = '\t\n\a\b\f\r\v'

# ---------------------------------------------------------------------
# 异常字符
# - 字节编码，包括单字节与多字节 unicode 编码，均有大量的字符无法正常显示，且
# 无对应的打印文本，这部分字符需要被剔除。
# - 此外，仍有大量的可打印字符，由于出现概率极低，且对中文处理作用极小，可以删除。

# 一、单字节字符：
# 即一个字节表示的字符，\x00~\xff，其中有一部分转义字符不打印，且非 # \t\n\r。
# 因此需要作为异常字符剔除掉，主要包括：\x00~\x08，\x0e~\x1f，\x7f~\x9f，\xa1~\xff
# 剩余的单字节字符参考 ascii 码表
ASCII_EXCEPTION_PATTERN = '[^\x09-\x0d\x20-\x7e\xa0£¥©®°±×÷]'

# 二、UNICODE 字符
# 即多个字节组成的字符，其中，囊括了各种语言的各种符号，这里我们只关心常用中文字符
# 以及相应的常用符号，单字节符号、标点符号等。而日文、俄文、拉丁、希腊、数学公式、
# 物理单位等符号 绝大多数不常用的都被丢弃。其中 㐀-䶵 指的是另一个汉字字符集
# 仅保留了常用符号，数字标识，如 ① 等
UNICODE_EXCEPTION_PATTERN = '[^‐-”•·・…‰※℃℉Ⅰ-ⅹ①-⒛\u3000-】〔-〞㈠-㈩一-龥﹐-﹫！-～￠￡￥]'
EXCEPTION_PATTERN = ASCII_EXCEPTION_PATTERN[:-1] + UNICODE_EXCEPTION_PATTERN[2:]

# ---------------------------------------------------------------------
# 全角字母、数字、空格正则
FULL_ANGLE_ALPHABET = 'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９　'
HALF_ANGLE_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '

# ---------------------------------------------------------------------
# HTML 标签
HTML_TAG_PATTERN = '<[^<\u4E00-\u9FA5，。；！？、“”‘’（）—《》…●]+?>'

# ---------------------------------------------------------------------
# 中国身份证号
# 身份证共计18位，1,2位省份，3,4位城市，5,6位县区码，7~14位为出生日期，最后一位为校验码，做了严格限定
ID_CARD_PATTERN = r'(?<=[^0-9a-zA-Z])' \
                  r'((1[1-5]|2[1-3]|3[1-7]|4[1-6]|5[0-4]|6[1-5]|71|81|82|91)' \
                  r'(0[0-9]|1[0-9]|2[0-9]|3[0-4]|4[0-3]|5[1-3]|90)' \
                  r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-3]|5[1-7]|6[1-4]|7[1-4]|8[1-7])' \
                  r'(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])' \
                  r'\d{3}[0-9xX])' \
                  r'(?=[^0-9a-zA-Z])'
ID_CARD_CHECK_PATTERN = r'^(1[1-5]|2[1-3]|3[1-7]|4[1-6]|5[0-4]|6[1-5]|71|81|82|91)' \
                        r'(0[0-9]|1[0-9]|2[0-9]|3[0-4]|4[0-3]|5[1-3]|90)' \
                        r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-3]|5[1-7]|6[1-4]|7[1-4]|8[1-7])' \
                        r'(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX]$'

# ---------------------------------------------------------------------
# IP地址
# 0~255.0~255.0~255.0~255
IP_SINGLE = r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)'
IP_ADDRESS_PATTERN = ''.join(
    [r'(?<=[^0-9])(', IP_SINGLE, r'\.', IP_SINGLE, r'\.', IP_SINGLE, r'\.', IP_SINGLE, ')(?=[^0-9])'])

# ---------------------------------------------------------------------
# 地名表达式
# 除中国地名表外，还有大量的地名未进行识别，采用正则匹配。然而仍然有一些特例：
# “城”字结尾的名词有不少房地产楼盘
LOCATION_CONTINENT_PATTERN = '(亚|欧|非|北美|中(南)?美|南美|拉丁美|南极|大洋)洲'  # 大洲
LOCATION_OCEAN_PATTERN = '(东|西|南|北)?(太平|大西|印度|北冰)洋'  # 大洋
LOCATION_INTER_REGION_PATTERN = '((东|西|南|北|中|东南|中北)亚|(东|西|南|北|中)欧|(东|西|北)非|拉美|北美|南美|(中|近|远)东)'  # 国际区域名词
LOCATION_KEYWORDS_PATTERN = CHINESE_CHAR_PATTERN + '+[县市镇村区山州路河城湖岛港江省湾乡街庄堡国寺桥溪岭海郡]'  # 尾缀词地名

# 各种不同类型的地名可以自由添加组合
LOCATION_PATTERN = '^(' + '|'.join(
    [LOCATION_CONTINENT_PATTERN, LOCATION_OCEAN_PATTERN,
     LOCATION_INTER_REGION_PATTERN, LOCATION_KEYWORDS_PATTERN]) + ')$'

# ---------------------------------------------------------------------
# 金额表达式 
# 裁判文书金额解析的正则
# '(\d[,，\d]*\.?\d+|[一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾两][一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾两〇O零百千万亿佰仟]*?)
# [百千万亿佰仟]*?美?元
# ((\d[,.，\d]*|[一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾两零][一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾两〇O零百千万亿佰>仟]*?)角)?
# ((\d[,.\d]*|[一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾两零][一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾两〇O零百千万亿佰仟]*?)分)?'

# 存在一定的错误金额字符串依然能够解析并通过的情况
CHINESE_NUM = '[一二三四五六七八九壹贰叁弎仨肆伍陆柒捌玖俩两零]'  # 金额数字
CHINESE_UNIT = '[〇O零十百千万亿兆拾佰仟萬億]'  # 金额数字单位
CURRENCY_CASE = r'(块(钱)?|元((人民|港|日|澳|韩|(新)?台)币)?|(人民|港|日|澳|韩|(新)?台)币|圆(整)?|' \
                r'(美|港|澳门|日|韩|缅|马|新加坡|欧|加|新西兰|澳|澳大利亚)元|美(金|刀)|英镑|马克|法郎|卢布|泰铢)'

CHI_N = CHINESE_NUM
CHI_U = CHINESE_UNIT

# 标准金额数字格式 7,129,012.02元
MONEY_PATTERN_1 = r'((\d{1,3}([,，]\d{1,3})*(\.\d{0,2})?)' + CURRENCY_CASE + ')'
# 纯数字格式 340000.0元
MONEY_PATTERN_2 = r'((\d{1,12}(\.\d{0,2})?)' + CURRENCY_CASE + ')'
# 中文金额格式 一万二千三百四十五
CHINESE_MONEY_PATTERN = ''.join(['(((', CHI_N, '?', CHI_U, '{1,2})*', CHI_N, '?)'])
# 正式文本中文金额格式 一万二千三百四十五元
MONEY_PATTERN_3 = CHINESE_MONEY_PATTERN + CURRENCY_CASE + '(' + CHI_N + '[角|毛])?(' + CHI_N + '分)?)'
# 口语文本中文金额格式 “三十五块八毛”，但不允许 “三十五块” 或 “三十五块八” 出现：有歧义
MONEY_PATTERN_4 = CHINESE_MONEY_PATTERN + '(块)' + '(' + CHI_N + '[角|毛])(' + CHI_N + '分)?)'
# 数字+汉字单位格式 9300万元  1.2万元  9佰元
MONEY_PATTERN_5 = r'(\d{1,4}(\.\d{0,4})?' + CHI_U + CURRENCY_CASE + ')'

MONEY_PATTERN = '(' + '|'.join(
    [MONEY_PATTERN_1, MONEY_PATTERN_2,
     MONEY_PATTERN_3, MONEY_PATTERN_4, MONEY_PATTERN_5]) + ')'

# ---------------------------------------------------------------------
# 中文括号
PARENTHESES_PATTERN = '{}「」[]【】()（）<>《》〈〉『』〔〕'

# ---------------------------------------------------------------------
# 标点符号
PUNCTUATION_PATTERN = ''

# ---------------------------------------------------------------------
# 腾讯QQ号
QQ_PATTERN = '(?<=[^0-9])([1-9][0-9]{5,10})(?=[^0-9])'
STRICT_QQ_PATTERN = r'(qq|QQ|\+q|\+Q|加q|加Q|q号|Q号)'
# STRICT_QQ_PATTERN = '([qQ]{2}[:： ]{0,5}[1-9][0-9]{5,10})(?=[^0-9])'

# ---------------------------------------------------------------------
# 冗余字符处理
# 文本中有连续的 “哈哈哈哈哈” 等字符串，需要删除冗余字符串，返回为 “哈”
REDUNDANT_PATTERN = ' -\t\n啊哈呀~\u3000\xa0•·・'

# ---------------------------------------------------------------------
# 纯数字格式，用于过滤停用词时，过滤掉纯数字（包括汉字数字）
# 融合了百分比格式、序数词，形容词（数*、*余等），负数，数字范围等，还差分数表
# 示未添加，如 “三十分之一”
BASE_NUMBER_PATTERN = '[' + CHINESE_NUM[1:-1] + CHINESE_UNIT[1:-1] + r'点\d\%％\.\,．多余几]+'
NUMBER_PATTERN = r'^((十|百|千|万)分之|第|数|好|\-)?' + BASE_NUMBER_PATTERN + r'([\~\-～－至]?' + BASE_NUMBER_PATTERN + ')?(多|余)?$'

# 纯数字格式（不包括汉字数字）
# 融合了整数、小数、百分比等
PURE_NUMBER_PATTERN = r'\-?\d+(\.\d+)?(%|％)?'

# ---------------------------------------------------------------------
# 时间词汇，用于停用词过滤时，将时间词汇过滤掉
# 1. 时间格式仅用于滤除具体确切的时间点和时间段，如“2019年6月30日”，“第一季度”，
#   “18:30:51”，“3~4月份”，“清晨”，“年前” 等等，此类词汇描述了具体的时间，在语言中
#   一般作为时间状语存在，因此在停用词滤除中，需要将该部分词汇滤除。
# 2. 但不滤除模糊的时间范围，如“三十年”，“六七个月”，“十周”，“四日” 等等，这些时间
#   描述了一个模糊的时间段，并没有确切的指代，在语言中一般做宾语，补语，主语等，因此
#   在停用词滤除中，一般不将此类词汇滤除。
# 3. 有些词汇含义指代不明，如“三十一日”，具体指某月 31日，还是31天的时间，并不确切，
#   此时不予滤除。
# 4. 节日名称不予滤除，如“圣诞节”、“除夕夜”，尽管其指示具体的时间点，但是一般做名词性
#   成分，因此不予滤除。

# 时分秒格式
HO_N = r'([01]?\d|2[01234])'  # 时 数字格式
MI_N = r'[012345]?\d'  # 分 数字格式
SE_N = r'[012345]?\d'  # 秒 数字格式
HMS_GAP = '[:：]'
HMS_PATTERN_1 = '^(' + HO_N + HMS_GAP + MI_N + '(' + HMS_GAP + SE_N + ')?)$'  # 纯数字格式时分秒，或时分
HMS_PATTERN_2 = '^(' + HO_N + '(点|时|小时)(' + MI_N + '分(钟)?(' + SE_N + '秒(钟)?)?)?)$'  # 带汉字时分秒
HMS_PATTERN_3 = '^(' + HMS_PATTERN_1 + r'[\-\~—]{1,2}' + HMS_PATTERN_1 + ')$'  # 时间段
# HMS_PATTERN_4 = '^([012]?\d点)$'  # 有一定前提条件，即前后必须也有时间词汇

# 年月日格式
YE_N = r'[12]?\d{2,3}'  # 年份数字格式
MO_N = r'([0]?\d|1[012])'  # 月份数字格式
MO_C = r'(元|正|腊|一|二|三|四|五|六|七|八|九|十(一|二)?)'  # 月份汉字格式
DA_N = r'([012]?\d|3[01])'  # 日数字格式
YMD_GAP = r'[\-\~— ～\.]{1,2}'
SPAN_GAP = r'[\~\-～－至]'

YMD_PATTERN_1 = '^((公元(前)?)?' + YE_N + '年(初|底|中)?)?((' + MO_N + '|' + MO_C + ')月(份|底|初)?)?(' + DA_N + '[日号])?$'  # 带汉字年月日
YMD_PATTERN_2 = '^(' + YE_N + YMD_GAP + MO_N + '(' + YMD_GAP + DA_N + ')?)$'  # 纯数字年月日，或年月
YMD_PATTERN_3 = '^(' + MO_N + YMD_GAP + DA_N + '(' + YMD_GAP + YE_N + ')?)$'  # 纯数字月日年，或月日
YMD_PATTERN_4 = '^((公元(前)?)?' + r'(([12]?\d|(二)?十(一|二|三|四|五|六|七|八|九)?)世纪)?((\d0|(一|二|三|四|五|六|七|八|九)十)年代)?(初|末)?' + ')$'  # 世纪，年代
YMD_PATTERN_5 = '^(一|二|三|四|五|六|七|八|九|零|〇|○|0){4}年$'

# 年月日-时分秒合并格式
YMD_HMS_PATTERN = '^(' + YMD_PATTERN_2[1:-1] + r'([\-\~\—]{1,2})?' + HMS_PATTERN_1[1:-1] + ')$'

# 农历日期
LUNAR_PATTERN = '((闰)?(元|正|腊|一|二|三|四|五|六|七|八|九|十(一|二)?)月|大年)(初(一|二|三|四|五|六|七|八|九|十)|(一|二|三|四|五|六|七|八|九|十){2,3})'

# 时间段
# 年时间段
YEAR_SPAN_PATTERN = '^' + YE_N + SPAN_GAP + YE_N + '年(代)?$'
# 月时间段
MONTH_SPAN_PATTERN = '^' + MO_N + SPAN_GAP + MO_N + '月(份)?$'
# 日时间段
DAY_SPAN_PATTERN = '^' + DA_N + SPAN_GAP + DA_N + '日$'

# 季节格式
SEASON_PATTERN = '((春|夏|秋|冬){1,2}(季|天|日)|(第)?(一|二|三|四)(季度)(末)?)'

# 星期格式
WEEK_PATTERN = '((上(半)?|下(半)?|这|本|前|今|当|上上|下下)?(星期|周)(六日|一|二|三|四|五|六|日|七|天|末|初)?(时)?)'

# 常见时间短语
COMMON_TIME_PATTERN_1 = '^(年|月|日|时)$'
COMMON_YEAR_PATTERN = r'(昔|翌|头(一|两|几|些)?|(大)?前(一|半|两|几|些)?|近(一|两|几|些)?|这(一|两|几|些)?|那(一|两|几|些)?|上(半)?|下(半)?|(大)?后(一|半|两|几|些)?|同|当|早(一|两|几|些)?|每|去|今|往|本|次|明|明后)?年(中|度|初|前|末|底|终|内)?'
COMMON_MONTH_PATTERN = r'(下(个)?|首(个)?|前(两|几)?|上(个)?|这(个)?|次|这(些|个)?|那(些|个)?|上半(个)?|下半(个)?|同|本|当|每)?月(份|中|度|初|末|底)?'
COMMON_DAY_PATTERN = r'(昔|首|前(一|两|几|些)?|翌|昨|次|今|往|明|平|即|往|半|旧|近(一|两|几|些)?|后(一|两|几|些)?|这(一|两|几|些)?|那(一|两|几|些)?|上半|下半|同|当|每(一)?)?(天|日)(前|后)?'
COMMON_TIME_PATTERN_2 = '(下|中|上)(午|旬)|近(期|日)|此前'
COMMON_TIME_PATTERN_3 = '(晚|早)(上|间)'
COMMON_TIME_PATTERN_4 = '(深|每|昨|前|今|午|后|半|上半|下半|春|当|夏|秋|冬)?夜(里|晚|间)?'
COMMON_TIME_PATTERN_5 = '(今|傍|昨|当)晚'
COMMON_TIME_PATTERN_6 = '(早|凌|今|清)晨|黎明'
COMMON_TIME_PATTERN_7 = '午(后|时)'

# 各类型的时间正则汇总，可根据需要进行增删
TIME_PATTERN = '(' + '|'.join(
    [COMMON_TIME_PATTERN_1,
     COMMON_YEAR_PATTERN, COMMON_MONTH_PATTERN, COMMON_DAY_PATTERN,
     COMMON_TIME_PATTERN_2, COMMON_TIME_PATTERN_3, COMMON_TIME_PATTERN_4,
     COMMON_TIME_PATTERN_5, COMMON_TIME_PATTERN_6, COMMON_TIME_PATTERN_7,
     WEEK_PATTERN, LUNAR_PATTERN, YMD_HMS_PATTERN, SEASON_PATTERN,
     YMD_PATTERN_1, YMD_PATTERN_2, YMD_PATTERN_3, YMD_PATTERN_4,
     YMD_PATTERN_5,
     HMS_PATTERN_1, HMS_PATTERN_2, HMS_PATTERN_3,
     YEAR_SPAN_PATTERN, MONTH_SPAN_PATTERN, DAY_SPAN_PATTERN, ]) + ')'

# ---------------------------------------------------------------------
# URL
URL_PATTERN = r'(?<=[^.])((?:(?:https?|ftp|file)://|(?<![a-zA-Z\-\.])www\.)' \
              r'[\-A-Za-z0-9\+&@\(\)#/%\?=\~_|!:\,\.\;]+[\-A-Za-z0-9\+&@#/%=\~_\|])' \
              r'(?=[<\u4E00-\u9FA5￥，。；！？、“”‘’>（）—《》…● ])'


#######################################################################
# 针对 time_parser 的正则字符串
# 字符串操作
# 年
LIMIT_YEAR_STRING = r'(前|今|明|去|同|当|后|大前|本|次|上(一)?)年'
LUNAR_YEAR_STRING = r'([一二三四五六七八九零〇]{2}|[一二三四五六七八九零〇]{4}|[12]\d{3}|\d{2})年'
YEAR_STRING = r'([12]?\d{2,3}|[一二三四五六七八九零〇]{2,4})年'

# 月
MONTH_NUM_STRING = r'(1[012]|[0]?[1-9]|十[一二]|[一二三四五六七八九十])'  # 1~12 std month num
MONTH_STRING = MONTH_NUM_STRING + r'月(份)?'
MONTH_NUM_STRING = MONTH_NUM_STRING[:-2] + r'两])'  # 1~12 order month num
BLUR_MONTH_STRING = r'(初|[一]开年|伊始|末|尾|终|底|[上下]半年|[暑寒][假期]|[前中后]期)'
LUNAR_MONTH_STRING = r'(闰)?([正一二三四五六七八九十冬腊]|十[一二]|[1-9]|1[012])月'
LIMIT_MONTH_STRING = r'([下上](个)?|同|本|当|次)月'
SELF_EVI_LUNAR_MONTH_STRING = r'((闰)?[正冬腊]|闰([一二三四五六七八九十]|十[一二]|[1-9]|1[012]))月'

# 周
WEEK_NUM_STRING = r'[一二两三四五六七八九十0-9]{1,3}'  # 1~52
WEEK_STRING = r'(周|星期|礼拜)'

# 日
DAY_NUM_STRING = r'(([12]\d|3[01]|[0]?[1-9])|([一二]?十)?[一二三四五六七八九]|(三十)?[一]|[二三]?十)'  # 1~31
DAY_STRING = DAY_NUM_STRING + r'[日号]'
BLUR_DAY_STRING = r'([上中下]旬|初|中|底|末)'
# 允许 `初8` 阿拉伯数字出现，但不允许 `廿2`、`23` 等作为农历`日`
LUNAR_SOLAR_DAY_STRING = r'((初|(二)?十|廿)[一二三四五六七八九]|[初二三]十|初([1-9]|10)|[12]\d|3[01]|[0]?[1-9])'
LUNAR_DAY_STRING = r'((初|(二)?十|廿)[一二三四五六七八九]|[初二三]十|初([1-9]|10))'
SELF_EVI_LUNAR_DAY_STRING = r'([初廿]([一二三四五六七八九十1-9]|10))'

# 时
HOUR_STRING = r'((十)?[一两二三四五六七八九]|[零〇十]|二十[一二三四]?|[01]?\d|2[01234])[时点]'
BLUR_HOUR_STRING = r'(凌晨|白天|清[晨|早]|黎明|一(大)?早|早[晨上]?|[上中下]午|午后|(傍)?晚[间上]?|[深半午]?夜[里间]?|[上下前后]半夜)'

# 分、秒
MIN_SEC_STRING = r'((零|〇|[一二三四五]?十)[一二三四五六七八九]|[二三四五]?十|[012345]?\d)'

# seg
I = '|'
LU = r'(农历)'
LU_A = absence(LU)

# appendix
TIME_POINT_SUFFIX = r'(左右|许)'
TIME_SPAN_SUFFIX = r'((之)?间)'
# TIME_DELTA_SUFFIX = r''

# 节气
SOLAR_TERM_STRING = r'(立春|雨水|惊蛰|春分|清明|谷雨|立夏|小满|芒种|夏至|小暑|大暑|'\
    r'立秋|处暑|白露|秋分|寒露|霜降|立冬|小雪|大雪|冬至|小寒|大寒)'

# 固定公历节日
FIXED_SOLAR_FESTIVAL = r'((元旦|十一)|(三八|五一|六一|七一|八一|国庆|圣诞)(节)?|'\
    r'((三八)?妇女|女神|植树|(五一)?劳动|(五四)?青年|(六一)?儿童|(七一)?建党|(八一)?建军|教师|情人|愚人|万圣|护士)节|'\
    r'地球日|三[\.•·・]?一五|双(十一|11)|(.{1,4})?消费者权益日)'
# 固定农历节日
FIXED_LUNAR_FESTIVAL = r'((春|填仓|上巳|寒食|清明|浴佛|姑姑|财神|下元|寒衣)节|'\
    r'(龙抬头|除夕)|' \
    r'(大年初[一二三四五六七八九十])|'\
    r'(端午|端阳|七夕|元宵|中秋|重阳|腊八|中元)(节)?)'
# 规律公历节日
REGULAR_FOREIGN_FESTIVAL = r'(感恩|母亲|父亲)节'

# time_delta 数字正则
DELTA_NUM_STRING = r'(([一两二三四五六七八九十百千万零]+点)?[一两二三四五六七八九十百千万零]+|([\d十百千万,]+\.)?[\d十百千万,]+)'
QUARTER_NUM_STRING = r'[一两二三四1-4]'

# 单个数字正则
SINGLE_NUM_STRING = r'[一两二三四五六七八九十\d]'

# time_delta 正则
YEAR_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'[多余]?(周)?年(多)?', I, '半年', I, SINGLE_NUM_STRING, '年半'])
SOLAR_SEASON_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'个(多)?季度'])
MONTH_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'(多)?个(多)?月', I, '俩月', I, '半(个(多)?)?月', I,
                              SINGLE_NUM_STRING, '个半月'])
WORKDAY_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'[多余]?(个)?(工作|交易)日'])
DAY_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'[多余]?[天日]', I, '半天', I, SINGLE_NUM_STRING, '天半'])
WEEK_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'[多余]?((个(多)?)?(星期|礼拜)|周(?!年))', I, r'俩(星期|礼拜)'])
HOUR_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'[多余]?(个(多)?)?(小时|钟头)', I,
                             '半(个(多)?)?(小时|钟头)', I, '俩(小时|钟头)', I, SINGLE_NUM_STRING, '个半(小时|钟头)'])
QUARTER_DELTA_STRING = ''.join([QUARTER_NUM_STRING, '刻钟'])
MINUTE_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'[多余]?分(钟)?(半)?', I, '半分钟', I,
                               SINGLE_NUM_STRING, '+分半(钟)?'])
SECOND_DELTA_STRING = ''.join([DELTA_NUM_STRING, r'[多余]?秒(钟)?'])


# 将时间进行转换
# DELTA_SUB = r'([之以]?[内前后上下来])'
DELTA_SUB = r'([之以]?[内前后来])'

########################################################################
# 时间 NER 字符规则
TIME_CHAR_STRING = ''.join(
    [r'(现在|开始|黎明|过去|',
     r'[102年月日3589647时午至天上个分今下\:\-点晚前一小后周起内以底三晨钟来半两凌当十份季去早多第五中初\.度二从六期旬到间四节号：',
     r'代\~\—春明昨星末秋之同·世纪本七九秒每次八夏/夜零正冬腊余工作元国清傍交易首 ()（）、万宵全暑头端庆旦－际消费者权益大里农历双财',
     r'近运深, ”夕〇几汛儿童劳动假圣诞壹感恩无数白百刻许左右的这])+'])
FAKE_POSITIVE_START_STRING = r'[起到至以开－\—\-\~]'  # 此字符串不可作为时间串的开始， `以来|开始` 为取首字
FAKE_POSITIVE_END_STRING = r'[到至－\—\-\~]'  # 此字符串不可作为时间串的结束

########################################################################
# 货币金额 NER 字符规则
MONEY_PREFIX_STRING = r'((将)?近|只有|仅|(大)?约(莫|合)?|大概|至少(要)?|不(到|足|超过)?|逾|高于|(高)?达(到)?|^上|(超)?过|超)'
MONEY_SUFFIX_STRING = r'(以上|以下|左右|上下)'

MONEY_BLUR_STRING = r'((大)?约(莫|合)?|大概|左右|上下)'
MONEY_MINUS_STRING = r'((将)?近|不(到|足|超过)?|以下)'
MONEY_PLUS_STRING = r'(至少(要)?|逾|高于|上|(超)?过|超|以上)'

MONEY_NUM_MIDDLE_STRING = r'[,， ]'
# 用于检测字符串是否有误，直接报错
MONEY_NUM_STRING = r'^[ \.多个数几百佰k千仟w万萬亿十拾兆〇O0-9零０-９一二两三四五六七八九壹贰俩叁弎仨肆伍陆柒捌玖]+$'

MONEY_KUAI_MAO_JIAO_FEN_STRING = r'[分角毛块]'
MONEY_PREFIX_CASE_STRING = r'(港币|人民币|(新)?台币)'
MONEY_SUFFIX_CASE_STRING = r'((分|角|毛|块|元)钱?|(人民|港|日|澳|(新)?台)币|圆(整)?|英镑|美(金|分|刀)|马克|法郎|卢布|泰铢|'\
                           r'元((人民|港|日|澳|韩|(新)?台)币)?|(美|港|澳门|日|韩|缅|马|新加坡|欧|加|新西兰|澳|澳大利亚)元)'

# MONEY_SPAN_GAP_START = r'(从)'
# MONEY_SPAN_GAP_MIDDLE = r'(\~+|\-+|～+|－+|至(?!少)|(?<![达不])到)'

MONEY_CHAR_STRING = r'((将)?近|只有|仅|(大)?约(莫|合)?|大概|至少(要)?|不(到|足|超过)?|逾|高于|(高)?达(到)?|^上|(超)?过|超|' \
                    r'以上|以下|左右|上下|港币|人民币|(新)?台币|(分|角|毛|块|元)钱?|(人民|港|日|澳|(新)?台)币|圆(整)?|英镑|' \
                    r'美(金|分|刀)|马克|法郎|卢布|泰铢|元((人民|港|日|澳|韩|(新)?台)币)?|(美|港|澳门|日|韩|缅|马|新加坡|欧|' \
                    r'加|新西兰|澳|澳大利亚)元|' \
                    r'[分角毛块 \.\,\-\~—－～，多个数几百佰k千仟w万萬亿十拾兆〇O0-9零０-９一二两三四五六七八九壹贰俩叁弎仨肆伍陆柒捌玖\(\)（）不含])+'


