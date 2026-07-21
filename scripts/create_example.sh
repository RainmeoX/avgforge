#!/bin/bash
# 创建《星轨之约》完整示例项目
set -e

AVGFORGE="/home/z/my-project/avgforge-dev/avgforge"
EXAMPLES_DIR="/home/z/my-project/avgforge-dev/examples"
PROJECT="$EXAMPLES_DIR/star-orbit-vow"

rm -rf "$PROJECT"

echo "=== 1. 创建项目 ==="
$AVGFORGE init "$PROJECT" \
    --name "星轨之约" \
    --author "AVGForge Demo" \
    --description "毕业前最后 30 天，与来自星轨观测站的少女相遇的故事。AVGForge 完整功能演示项目。"

cd "$PROJECT"

echo ""
echo "=== 2. 添加角色 ==="
$AVGFORGE char add "星野" --pos right --color-ring "#ffb6d9" --color-bg "#ffe4e6" --color-fg "#9f1239"
$AVGFORGE char add "我" --pos left --color-ring "#7fc8f8" --color-bg "#dbeafe" --color-fg "#1e40af"

echo ""
echo "=== 3. 添加场景 ==="
$AVGFORGE scene add "教室" --layer "天空:14:backgrounds/classroom/sky.png" --layer "远景:7:backgrounds/classroom/far.png" --layer "教室:2:backgrounds/classroom/room.png"
$AVGFORGE scene add "天台" --layer "天空:14:backgrounds/rooftop/sky.png" --layer "城市:7:backgrounds/rooftop/city.png" --layer "天台:2:backgrounds/rooftop/floor.png"
$AVGFORGE scene add "星轨观测站" --layer "宇宙:14:backgrounds/starry/cosmos.png" --layer "星云:7:backgrounds/starry/nebula.png" --layer "平台:2:backgrounds/starry/platform.png"
$AVGFORGE scene add "真结局" --layer "宇宙:1:backgrounds/ending/true.png"
$AVGFORGE scene add "普通结局" --layer "远方:1:backgrounds/ending/normal.png"
$AVGFORGE scene add "Bad_End" --layer "夜空:1:backgrounds/ending/bad.png"

echo ""
echo "=== 4. 添加变量 ==="
$AVGFORGE var add trust "信任度" --type number --scope project --persistence slot --default 0 --description "星野对主角的信任"
$AVGFORGE var add memory_count "回忆数量" --type number --scope project --persistence slot --default 0
$AVGFORGE var add promised "是否约定" --type boolean --scope project --persistence slot --default false
$AVGFORGE var add endings_unlocked "已解锁结局" --type string --scope project --persistence shared --default "" --description "跨周目记录"
$AVGFORGE var add play_count "游玩次数" --type number --scope system --persistence shared --default 0

echo ""
echo "=== 5. 添加章节 ==="
$AVGFORGE chapter add "第一章_相遇"
$AVGFORGE chapter add "第二章_相知"
$AVGFORGE chapter add "第三章_抉择"
$AVGFORGE chapter add "终章"

echo ""
echo "=== 6. 添加分支片段 ==="
$AVGFORGE frag add "第一章_相遇" "接受邀请"
$AVGFORGE frag add "第一章_相遇" "拒绝邀请"
$AVGFORGE frag add "第二章_相知" "陪伴"
$AVGFORGE frag add "第二章_相知" "寻找方法"
$AVGFORGE frag add "第三章_抉择" "随她而去"
$AVGFORGE frag add "第三章_抉择" "留下等待"
$AVGFORGE frag add "第三章_抉择" "恳求留下"
$AVGFORGE frag add "终章" "真结局"
$AVGFORGE frag add "终章" "普通结局"
$AVGFORGE frag add "终章" "Bad_End"

echo ""
echo "=== 7. 写入剧本 ==="

# 开始章节
cat > /tmp/script_start.rpy << 'EOF'
curtain close duration 0
scene 教室 with fade duration 1.0
curtain open duration 1.5
"毕业前 30 天。"
"教室里只剩下我一个人。"
"窗外的夕阳把整间教室染成了橘红色。"
show 星野 at right
"突然，天台的门被推开了。"
"一个银白色长发的少女站在门口，紫色的眼睛在夕阳下闪闪发光。"
星野 "你在这里啊。"
"我愣住了。"
"这个女孩，我从未见过。"
我 "你是……？"
星野 "我叫星野。来自星轨观测站。"
"星轨观测站？"
"我从未听说过这个地方。"
EOF
$AVGFORGE edit 开始/main --file /tmp/script_start.rpy

# 第一章
cat > /tmp/script_ch1.rpy << 'EOF'
scene 天台 with fade duration 1.0
show 星野 at right
星野 "每 120 年，星轨会经过地球一次。"
星野 "我搭上星轨来到这里，只能停留 30 天。"
"30 天……"
"正好是我毕业前的时间。"
星野 "在这 30 天里，我想多了解一些地球的故事。"
星野 "你愿意陪我吗？"
menu "怎么回答":
    "当然愿意" -> call 接受邀请
    "我为什么要帮你？" -> call 拒绝邀请
EOF
$AVGFORGE edit 第一章_相遇/main --file /tmp/script_ch1.rpy

# 接受邀请
cat > /tmp/script_ch1_accept.rpy << 'EOF'
$ trust += 5
星野 "谢谢你！"
"她的眼睛亮了起来，像两颗小星星。"
"从那天起，我开始带她游览这个小镇。"
"图书馆、咖啡馆、公园……"
"每一个地方，她都看得津津有味。"
EOF
$AVGFORGE edit 第一章_相遇/接受邀请 --file /tmp/script_ch1_accept.rpy

# 拒绝邀请
cat > /tmp/script_ch1_refuse.rpy << 'EOF'
$ trust -= 3
星野 "……也是呢。"
"她的眼神黯淡了一下。"
"但第二天，她又出现在了天台。"
星野 "我又来了。"
星野 "因为我实在没有其他人可以找了。"
"看着她孤独的样子，我叹了口气。"
我 "好吧，我陪你。"
$ trust += 2
EOF
$AVGFORGE edit 第一章_相遇/拒绝邀请 --file /tmp/script_ch1_refuse.rpy

# 第二章
cat > /tmp/script_ch2.rpy << 'EOF'
scene 星轨观测站 with fade duration 1.5
show 星野 at right
"两周过去了。"
"星野带我来到了星轨观测站。"
"那是一个悬浮在山顶的银色平台。"
星野 "再过 15 天，星轨就要离开了。"
星野 "我必须搭上它，否则会永远消散。"
"消散？"
"我握紧了拳头。"
menu "怎么办？":
    "我会陪你到最后" -> call 陪伴
    "一定有办法让你留下" -> call 寻找方法
EOF
$AVGFORGE edit 第二章_相知/main --file /tmp/script_ch2.rpy

# 陪伴
cat > /tmp/script_ch2_stay.rpy << 'EOF'
$ trust += 5
$ memory_count += 10
星野 "谢谢你。"
"剩下的 15 天，我们形影不离。"
"看日出、数星星、聊彼此的世界……"
"每一刻都珍贵得像是要碎掉。"
EOF
$AVGFORGE edit 第二章_相知/陪伴 --file /tmp/script_ch2_stay.rpy

# 寻找方法
cat > /tmp/script_ch2_find.rpy << 'EOF'
$ trust += 2
"我翻遍了图书馆的所有天文书籍。"
"询问了每一个可能知道的人。"
"但答案都是一样的——"
"星轨的能量，无法在地球维持她的存在。"
星野 "别找了。"
星野 "我已经接受了这个事实。"
EOF
$AVGFORGE edit 第二章_相知/寻找方法 --file /tmp/script_ch2_find.rpy

# 第三章
cat > /tmp/script_ch3.rpy << 'EOF'
scene 星轨观测站 with fade duration 1.0
show 星野 at right
"最后一天。"
"星轨的光芒已经出现在天际。"
星野 "时间到了。"
星野 "谢谢你这 30 天的陪伴。"
"她的声音很平静，但我看到她的手在颤抖。"
menu "最后的抉择":
    "带我一起走" -> call 随她而去
    "我会等你回来" -> call 留下等待
    "求你留下来" -> call 恳求留下
EOF
$AVGFORGE edit 第三章_抉择/main --file /tmp/script_ch3.rpy

# 真结局
cat > /tmp/script_true.rpy << 'EOF'
$ promised = true
scene 真结局 with fade duration 2.0
"我握住了她的手。"
我 "我跟你走。"
星野 "你……你确定吗？"
"我点了点头。"
"星轨的光芒笼罩了我们。"
"地球在我脚下越来越小。"
"但我的手，始终握着她的。"
"——星轨之约，永不分离。——"
EOF
$AVGFORGE edit 终章/真结局 --file /tmp/script_true.rpy

# 普通结局
cat > /tmp/script_normal.rpy << 'EOF'
scene 普通结局 with fade duration 2.0
"我看着她踏上星轨。"
星野 "再见。"
星野 "下一个 120 年，我还会来的。"
"她化作一道光，消失在星空中。"
"我站在天台上，看着那颗最亮的星。"
"120 年……"
"那是我无法到达的远方。"
"但我知道，她还在那里。"
EOF
$AVGFORGE edit 终章/普通结局 --file /tmp/script_normal.rpy

# Bad End
cat > /tmp/script_bad.rpy << 'EOF'
scene Bad_End with fade duration 2.0
星野 "留下来？"
星野 "……我做不到。"
星野 "如果留下来，我会在 24 小时内消散。"
"但她没有听我的话。"
"零点的钟声响起时，她化作漫天的光点。"
"其中一颗，特别亮，特别近。"
"它停在了天台的正上方，再也没有移动过。"
"后来，我毕业、工作、老去。"
"每个失眠的夜晚，我都会去天台。"
"抬头，看着那颗星。"
"我知道，那是她。"
"她还在那里。"
"只是，再也不会回答我了。"
EOF
$AVGFORGE edit 终章/Bad_End --file /tmp/script_bad.rpy

echo ""
echo "=== 8. 项目信息 ==="
$AVGFORGE info

echo ""
echo "=== 9. 项目验证 ==="
$AVGFORGE check

echo ""
echo "=== 10. 生成流程图 ==="
$AVGFORGE preview graph

echo ""
echo "=== 完成！ ==="
echo "项目路径: $PROJECT"
