
CREATE TABLE `match`
(
    `id`         int(11)     NOT NULL AUTO_INCREMENT,
    `match_id`   varchar(32) NOT NULL COMMENT '比赛id',
    `start_at`   datetime    NOT NULL COMMENT '比赛开始时间',
    `match_time` int(11)     NOT NULL COMMENT '比赛时长',
    `state`      varchar(32) not null default 'init' comment '数据状态',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_match_id` (`match_id`),
    KEY `idx_state` (`state`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
   COMMENT ='比赛表';

CREATE TABLE `player`
(
    `id`             int(11)     NOT NULL AUTO_INCREMENT,
    `player_id`      varchar(32) NOT NULL COMMENT '选手id',
    `player_name`    varchar(32) NOT NULL COMMENT '选手名称',
    `player_real_name` varchar(32) NOT NULL COMMENT '选手真实姓名',
    `player_grade`   varchar(32) NOT NULL COMMENT '选手星级',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT ='选手表';

CREATE TABLE `match_ban`
(
    `id`         int(11)     NOT NULL AUTO_INCREMENT,
    `match_id`   varchar(32) NOT NULL COMMENT '比赛id',
    `champion_id` varchar(32) NOT NULL COMMENT '英雄id',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_match_id` (`match_id`, `champion_id`),
    KEY `idx_champion_id` (`champion_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT ='比赛禁用英雄表';


CREATE TABLE `match_detail`
(
    `id`         int(11)     NOT NULL AUTO_INCREMENT,
    `match_id`   varchar(32) NOT NULL COMMENT '比赛id',
    `player_id`  varchar(32) NOT NULL COMMENT '选手id',
    `svp`        int(11)     NOT NULL COMMENT '是否为svp',
    `mvp`        int(11)     NOT NULL COMMENT '是否为mvp',
    `champion_id` varchar(32) NOT NULL COMMENT '英雄id',
    `position`   varchar(32) NOT NULL COMMENT '位置',
    `score`      int(11)     NOT NULL COMMENT '得分',
    `team_id`    varchar(32) NOT NULL COMMENT '队伍id',
    `win`        int(11)     NOT NULL COMMENT '是否胜利',
    `kill`       int(11)     NOT NULL COMMENT '击杀数',
    `death`      int(11)     NOT NULL COMMENT '死亡数',
    `assist`     int(11)     NOT NULL COMMENT '助攻数',
    `gold_earned` int(11)    NOT NULL COMMENT '金币数',
    `double_kills` int(11)   NOT NULL COMMENT '双杀',
    `triple_kills` int(11)   NOT NULL COMMENT '三杀',
    `quadra_kills` int(11)   NOT NULL COMMENT '四杀',
    `penta_kills` int(11)    NOT NULL COMMENT '五杀',
    `godlike`     int(11)     NOT NULL COMMENT '超神',
    `champion_damage` int(11) NOT NULL COMMENT '英雄伤害',
    `damage_taken` int(11)   NOT NULL COMMENT '承受伤害',
    `ward_placed` int(11)    NOT NULL COMMENT '插眼数',
    `gold_earned_percent` float not null default 0 comment '经济比',
    `champion_damage_percent` float not null default 0 comment '伤害比'
    PRIMARY KEY (`id`),
    KEY `idx_match_id` (`match_id`),
    KEY `idx_player_id` (`player_id`),
    UNIQUE KEY `match_player` (`match_id`, `player_id`),
    KEY `idx_champion_id` (`champion_id`),
    KEY `idx_position` (`position`),
    KEY `idx_team_id` (`team_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT ='比赛详情表';

CREATE TABLE `champion`
(
    `id`         int(11)     NOT NULL AUTO_INCREMENT,
    `champion_id` varchar(32) NOT NULL COMMENT '英雄id',
    `champion_name` varchar(32) NOT NULL COMMENT '英雄名称',
    `champion_icon` varchar(1024) NOT NULL COMMENT '英雄图标',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_champion_id` (`champion_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT ='英雄表';
