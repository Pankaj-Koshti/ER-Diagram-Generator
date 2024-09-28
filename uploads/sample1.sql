create table users
    (user_id          varchar(10),
     username         varchar(50),
     email            varchar(100),
     password         varchar(255),
     created_at       datetime default current_timestamp,
     primary key (user_id)
    );

create table products
    (product_id       varchar(10),
     product_name     varchar(100) not null,
     price            decimal(10),
     stock_quantity   numeric(2),
     created_at       datetime default current_timestamp,
     primary key (product_id)
    );

create table categories
    (category_id      varchar(10),
     category_name    varchar(50) not null unique,
     description      text,
     primary key (category_id)
    );

create table orders
    (order_id         varchar(10),
     user_id          varchar(10),
     order_date       datetime default current_timestamp,
     primary key (order_id),
     foreign key (user_id) references users (user_id)
    );

create table order_items
    (order_item_id    varchar(10),
     user_id          varchar(10),
     order_id         varchar(10),
     product_id       varchar(10),
     quantity         varchar(100),
     total_price      numeric(2),
     primary key (order_item_id),
     foreign key (user_id) references users (user_id),
     foreign key (order_id) references orders (order_id),
     foreign key (product_id) references products (product_id)
    );

create table product_categories
    (product_id       varchar(10),
     category_id      varchar(10),
     primary key (product_id),
     foreign key (product_id) references products (product_id),
     foreign key (category_id) references categories (category_id)
    );
