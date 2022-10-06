create database CommentsDB character set gbk;
use CommentsDB;
create table comments (
	com_id int unsigned auto_increment primary key comment '编号',
    name varchar(20) not null comment '用户名',
    time varchar(20) not null comment '评论时间',
    content varchar(10000) not null comment '内容'
)engine=InnoDB comment='商品评论';
select * from comments;