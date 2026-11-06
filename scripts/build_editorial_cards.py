#!/usr/bin/env python3
"""Compile explicitly authored, contextual key-word cards; never edit manuscripts."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
# paragraph | exact anchor | dictionary form | kind | contextual Chinese gloss | English gloss
CARDS={
'01':[
(9,'warte gern auf dich','warten auf + Akk.','verb','等候、等待。这里是“我很乐意等你”；auf dich 是“等你”，不是“在你上面”。','to wait for; here: I am happy to wait for you'),
(20,'möchte','mögen · möchte','verb','想要、希望，语气比直接说 wollen 更柔和。这里是 Leon 希望 Max 暖和一点。','would like; here: wishes Max to be warm'),
(20,'dir warm ist','jemandem ist warm','phrase','某人觉得暖和。dir 指 Max：“让你暖和一点”；这里不是“你这个人很热情”。','someone feels warm; dir refers to Max'),
(3,'Café','das Café · die Cafés','noun','咖啡馆。注意 Café 是见面的场所；Kaffee 才是杯子里的咖啡。','café; the place, as opposed to Kaffee, the drink'),
(28,'lässt seine Hand nicht los','loslassen','verb','松开、放手。可分动词：lässt … los；nicht 否定整个动作，即“没有松开他的手”。','to let go; here: does not let go of his hand'),
],
'02':[
(18,'Handschuhe','der Handschuh · die Handschuhe','noun','手套。这里用复数，Max 没戴手套，所以手很冷。','gloves'),
(19,'vergessen','vergessen','verb','忘记、遗忘。habe … vergessen 表示已经忘了；sie 指前文的手套。','to forget; here: left the gloves at home'),
(33,'Bahn','die Bahn · die Bahnen','noun','轨道交通车辆；这段是在电车站，指 Max 要乘坐的电车，不是抽象的“路线”。','tram in this scene'),
(54,'verbringen','verbringen','verb','度过（时间）。Zeit / fünf Minuten mit jemandem verbringen：与某人共度时光。','to spend time; here: spend five more minutes with you'),
(61,'öffnen sich','sich öffnen','verb','打开。Die Türen öffnen sich 是“车门开了”，不是“车门打开自己”。','to open; here: the doors open'),
(75,'Das ist mir egal','jemandem egal sein','phrase','某人不在意、觉得无所谓。Max 不介意 Leon 的房间小；这里不是在敷衍或嫌弃 Leon。','I do not mind; here: the small apartment is no problem'),
],
'03':[
(30,'Vertrau mir','vertrauen + Dativ','verb','相信、信任。Vertrau 是对 du 的命令式；mir 是第三格：“相信我”。','trust me'),
(43,'gut aussehe','aussehen','verb','看起来、外貌显得。aussehen 可分：ich sehe … aus；这里 Max 在开玩笑说自己长得好看。','to look; here: to look good'),
(53,'Schmeckt es dir','schmecken + Dativ','verb','尝起来合某人的口味。这里问“你觉得好吃吗”；dir 是品尝的人。','does it taste good to you?'),
(58,'Salz','das Salz','noun','盐。Max 忘记放盐，是这顿意大利面味道不对的原因。','salt'),
(67,'retten','retten','verb','挽救。这里是给晚餐补救，不是抢救一个人。','to save; here: rescue the meal'),
(140,'Versprochen','versprechen','verb','答应、承诺。单独说 Versprochen? 是“说好了？”；回答 Versprochen. 是“说好了”。','promise; here: Is that a promise?'),
(156,'passe gut darauf auf','aufpassen auf + Akk.','verb','好好照顾、留意。passe … auf 来自可分动词 aufpassen；darauf 回指 Max 留下的“心”。','to take good care of it; it refers to Max’s heart'),
],
'04':[
(17,'höre dir doch zu','zuhören + Dativ','verb','听某人说话。höre … zu 是可分动词；这里是“我当然在认真听你说呀”。','to listen to you; here: I am listening, of course'),
(52,'fällt aus','ausfallen','verb','取消、停运。这里是末班电车不运行了，不是“从车上掉下来”。','to be cancelled; here: the last tram is not running'),
(61,'lasse dich doch nicht','jemanden etwas tun lassen','phrase','让某人做某事。整句是否定：“我可不会让你冒着这场雨走回家”。','I would not let you walk home in this rain'),
(80,'Bett','das Bett · die Betten','noun','床。groß genug für zwei 表示足够两个人睡，是两人接下来对话的重点。','bed; here: large enough for two people'),
(98,'näher kommen','näher kommen','verb','靠近一些。näher 是 nah 的比较级；这里 Max 在征求靠近 Leon 的许可。','to come closer'),
(106,'schlägt','schlagen','verb','这里指心脏跳动。Sein Herz schlägt … 是“他的心跳得……”，不是“他的心在打人”。','to beat; here: his heart is beating'),
],
'05':[
(35,'Rührei','das Rührei','noun','炒鸡蛋。这是 Max 打算做的早餐，不是煮鸡蛋或煎荷包蛋。','scrambled eggs'),
(48,'Unterschied','der Unterschied · die Unterschiede','noun','区别、差别。Leon 问的是 Max 能不能分清盐和糖。','difference; here: the difference between salt and sugar'),
(76,'Hälfte','die Hälfte · die Hälften','noun','一半。Die Hälfte für dich 是把食物的一半分给对方。','half; here: half for you'),
(131,'planst aber weit voraus','vorausplanen','verb','提前计划。这里 Leon 带点惊讶地说 Max 已经想得很长远了；aber 在此加强语气。','to plan ahead; here: you really are planning far ahead'),
(153,'festhalten','festhalten','verb','握紧、抱住不放。这里指 Max 还想再抱 Leon 一会儿，不是“记录下来”。','to hold on to; here: keep holding Leon'),
(180,'verliebe ich mich','sich verlieben in + Akk.','verb','爱上某人。这里是“我也许真的正在爱上他”，强调感情正在发生变化，而不只是“我爱他”。','to fall in love; here: perhaps I really am falling for him'),
],
'06':[
(28,'Verspätung','die Verspätung · die Verspätungen','noun','延误、晚点。Meine Bahn hatte Verspätung：Max 的电车晚点了。','delay; here: the tram was delayed'),
(28,'Akku leer','der Akku · die Akkus','noun','电池。mein Akku war leer 是“我手机没电了”，不是电池不见了。','battery; here: the phone battery was dead'),
(53,'mir Sorgen um dich gemacht habe','sich Sorgen machen um + Akk.','verb','担心某人。Leon 生气的关键原因是担心 Max 出了事，而不只是讨厌他迟到。','to worry about someone; here: I was worried about you'),
(62,'hättest mir wenigstens eine Nachricht schicken können','hätte … schicken können','phrase','你本来至少可以给我发条消息。这里回顾过去没有做、但本可以做的事，不是在问现在能否发消息。','you could at least have sent me a message'),
(68,'empfindlich','empfindlich','adjective','敏感的、容易受伤的。Leon 担心 Max 觉得自己反应太大；这里不是皮肤容易过敏。','sensitive; here: emotionally oversensitive'),
(158,'dich bei mir sicher fühlst','sich sicher fühlen','verb','感到安全、安心。这里说的是关系中的安心感，不是“确信某个事实”。','to feel safe; here: feel secure with me'),
],
'07':[
(35,'verletzen','verletzen','verb','伤害。这里指说话伤害了 Leon 的感情，并非身体受伤。','to hurt; here: hurt someone’s feelings'),
(46,'vermisse dich','vermissen + Akk.','verb','想念你。这里是因为对方不在身边而想他，不是“错过你说的话”。','to miss you'),
(50,'schon viel zu lange her','lange her sein','phrase','已经是很久以前了。viel zu lange 强调“太久”；Max 夸张地觉得昨天见面也已经隔了太久。','already far too long ago'),
(56,'vorbeikommen','vorbeikommen','verb','顺道来、过来看看。这里是 Max 问可不可以到 Leon 家来。','to come over; here: visit Leon at home'),
(70,'Stirn','die Stirn · die Stirnen','noun','额头。auf die Stirn küssen：亲吻某人的额头。','forehead'),
(71,'hatte ich sowieso vor','vorhaben','verb','打算、计划。hatte … vor 是过去式；这句表示“我本来就打算这样做”，即留下过夜。','to intend; here: I was planning to do that anyway'),
],
'08':[
(35,'Pfannkuchen','der Pfannkuchen · die Pfannkuchen','noun','薄煎饼。这里是早餐煎饼，单复数形式相同。','pancake; plural: Pfannkuchen'),
(38,'brennt','brennen','verb','燃烧；这里指煎饼快要焦了。Max 在提醒 Leon 注意锅里的食物。','to burn; here: the pancake is burning'),
(43,'Kohle','die Kohle','noun','煤、炭。Max 开玩笑说煎饼黑得已经成炭；这里不是口语中“钱”的意思。','coal; jokingly: the burnt pancake has turned to charcoal'),
(54,'schaffen sie es','es schaffen','verb','成功做到。这里是两人一起终于做出了四张漂亮的煎饼。','to manage to do something'),
(95,'uns streiten','sich streiten','verb','争吵。wir streiten uns 是“我们吵架”；不是与彼此断绝关系。','to argue with each other'),
(100,'einer Meinung sein','einer Meinung sein','phrase','意见一致。整句说“不必每件事都持相同意见”，并不表示不再相爱。','to agree; here: we do not have to agree on everything'),
(115,'Lieblingsort','der Lieblingsort · die Lieblingsorte','noun','最喜欢的地方。Max 说与 Leon 在一起时，家就是他最喜欢去的地方。','favourite place'),
],
'09':[
(45,'Zettel','der Zettel · die Zettel','noun','便条、小纸条。桌上的 Zettel 是 Max 留给 Leon 的出行提示。','note; here: a small written note'),
(65,'geheimnisvoll','geheimnisvoll','adjective','神秘的、卖关子的。这里是 Leon 在说 Max 一直不肯透露旅行目的地。','mysterious; here: keeping the surprise secret'),
(106,'kaum','kaum','adverb','几乎不。kaum sehen 意思是两人忙得几乎见不到面，不是“看不清对方”。','hardly; here: hardly see each other'),
(121,'Schachtel','die Schachtel · die Schachteln','noun','小盒子。它装着这次惊喜的关键物品——钥匙。','small box'),
(127,'Schlüssel','der Schlüssel · die Schlüssel','noun','钥匙。这里既是房门钥匙，也是 Max 邀请 Leon 把这里当成家的信号。','key; here: a key to Max’s home'),
(145,'dich bei mir zu Hause fühlst','sich zu Hause fühlen','verb','感到像在自己家一样自在、有归属感。这里不只是确认 Leon 身处哪一间房。','to feel at home; here: feel that you belong with me'),
],
'10':[
(14,'Bettkante','die Bettkante · die Bettkanten','noun','床沿。Max 坐到床边，准备叫 Leon 起床。','edge of the bed'),
(16,'Schlafmütze','die Schlafmütze · die Schlafmützen','noun','爱睡懒觉的人、小懒虫。这里是亲昵的称呼，不是在说一顶睡帽。','sleepyhead; an affectionate nickname here'),
(37,'Kartons','der Karton · die Kartons','noun','纸箱。这里指 Leon 搬家带来的大纸箱。','cardboard boxes'),
(56,'Bibliothek','die Bibliothek · die Bibliotheken','noun','图书馆。Max 夸张地说书多得像搬来了一整座图书馆。','library; jokingly, Leon has brought a whole library'),
(65,'aufräumen','aufräumen','verb','收拾、整理。这里 Max 要 Leon 自己整理好那些书。','to tidy up; here: put the books away'),
(124,'ausgepackt','auspacken','verb','拆箱、把东西从包装或箱子里拿出来。noch nicht alle ausgepackt 表示搬家箱子还没全拆完。','to unpack; here: not all the boxes have been unpacked yet'),
(142,'lebendig','lebendig','adjective','有生气的、鲜活的。Max 用它形容同居后的家热闹起来了，不是在判断房子是不是活物。','lively, full of life; here: the home feels lived in'),
],
'11':[
(13,'Taille','die Taille · die Taillen','noun','腰部。die Arme um seine Taille legen：把双臂环在他的腰间。','waist'),
(24,'überzeugen','überzeugen','verb','说服、使信服。这里是 Leon 开玩笑说：也许还得先赢得 Max 父亲的认可。','to convince; here: Leon wants to win Max’s father over'),
(110,'räuspert sich','sich räuspern','verb','清清嗓子。父亲用这个动作打断两人或引起注意，不是开口大声说话。','to clear one’s throat'),
(138,'verschüttet','verschütten','verb','把液体洒出、泼到外面。这里是把咖啡意外洒到包上；不是给人倒咖啡。','to spill; here: spill coffee over the bag'),
(195,'erleichtert','erleichtert','adjective','如释重负地、松了一口气。父母离开后 Max 放松下来，描述的是他的情绪。','relieved; here: Max breathes out with relief'),
(208,'Haarsträhne','die Haarsträhne · die Haarsträhnen','noun','一缕头发。Leon 把 Max 脸前的那缕头发拨开。','strand of hair'),
],
'12':[
(3,'Pfütze','die Pfütze · die Pfützen','noun','水坑。自行车从水坑里驶过，才会溅起水来。','puddle'),
(119,'Denkst du manchmal darüber nach','nachdenken über + Akk.','verb','思考、琢磨。denkst … nach 是可分结构；darüber 回指后面“十年后生活会怎样”这件事。','do you sometimes think about it; here: life ten years from now'),
(150,'dieselben Menschen','derselbe / dieselbe / dasselbe','phrase','同样的人。这里担心未来的彼此已不再是现在的自己，而不是说出现了另外两个人。','the same people; here: whether we will remain who we are now'),
(163,'kennenlernen','kennenlernen','verb','认识、逐渐了解。这里即使相识已久，仍想继续了解变化后的对方。','to get to know; here: keep getting to know one another'),
(172,'es nicht schaffen','es schaffen','verb','没能做到、没能一起走下去。这里担心的是关系的未来，不是问能不能完成眼前的某项工作。','not manage to make it; here: not make the relationship work'),
(304,'Sonst hätten wir uns vielleicht nie kennengelernt','sonst hätten … kennengelernt','phrase','不然我们也许永远不会认识。这里假设过去没洒那杯咖啡；hätten … kennengelernt 表达过去的假设，不是实际发生的事。','otherwise, we might never have met'),
(317,'Schicksal','das Schicksal · die Schicksale','noun','命运。这里是在问是否相信相遇是命中注定的。','fate, destiny'),
(328,'Zufall','der Zufall · die Zufälle','noun','偶然、巧合。这里和“命运”对照：那天走进咖啡馆也许只是偶然。','chance, coincidence'),
(335,'uns wieder füreinander entschieden','sich entscheiden für + Akk.','verb','再次选择彼此。haben … entschieden 是完成时；füreinander 指“为了彼此、选择彼此”，强调后来的主动选择。','to choose each other again'),
],
'epilogue':[
(27,'verzweifelt','verzweifelt','adverb','焦急地、急得不知所措地。这里 Max 快迟到了，正在着急找牙刷；不必理解成深重的绝望。','frantically; here: urgently looking for his toothbrush'),
(27,'Zahnbürste','die Zahnbürste · die Zahnbürsten','noun','牙刷。Max 一边准备出门一边找不到它，构成结尾的日常小插曲。','toothbrush'),
(28,'fluchen','fluchen','verb','咒骂、气恼地嘟囔。这里 Leon 听见 Max 因赶时间而抱怨。','to swear or curse in frustration'),
(31,'Versprechen','das Versprechen · die Versprechen','noun','承诺。这里是名词，指郑重的许诺；不是动词“承诺”的一次变位。','promise; a noun here'),
(33,'vertrauten Stimme','vertraut','adjective','熟悉的、亲切的声音。这里是带着亲近感的“熟悉”，不是“被委托的声音”。','a familiar voice'),
]}
chapters={}
for cid,rows in CARDS.items():
 ps=(R/f'content/season-01/{cid}.txt').read_text().split('\n\n');entries=[]
 for paragraph,anchor,term,kind,zh,en in rows:
  text=ps[paragraph-1];assert anchor in text,(cid,paragraph,anchor,text)
  entries.append({'paragraph':paragraph,'anchor':anchor,'occurrence':1,'term':term,'kind':kind,'zh':zh,'en':en,'example':text.rstrip('\n'),'origin':'editorial'})
 chapters[cid]=entries
out={'version':1,'origin':'editorial','label':{'zh':'本站补充','en':'Site-authored'},'selectionPolicy':{'zh':'优先解释影响当前句意理解的关键动词、名词及固定表达；每章少量标注，同章不反复标出同一用法。原文不变，原始笔记独立保留。','en':'A small selection of verbs, nouns and expressions that affect the meaning of the current scene. Manuscripts and original notes are preserved.'},'chapters':chapters}
(R/'content/learning-editorial.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Site-authored key cards:',sum(map(len,chapters.values())))
