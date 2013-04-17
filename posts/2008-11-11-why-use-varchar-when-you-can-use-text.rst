---
layout: post
title: "Why use a VARCHAR when you can use TEXT?"
date: 2008-11-11T10:23:24-06:00
comments: false
categories: [Programming, PostgreSQL, Databases, InnoDB, MyISAM, sqlite, MySQL]
published: true
alias: [/blog/post/why-use-varchar-when-you-can-use-text]
---

Admit it, you've done it many times before: you create a database schema,
arbitrarily guessing at upper limits to the lengths of various columns, only to
later have to perform annoying schema upgrades as you change those columns to
fit real-world data.

If you're using PostgreSQL_, what you're doing is pointless.  There is quite
literally no performance benefit to be had, and possibly a performance penalty
as the database needs to check the length constraint.  This fact can even be
found `right here, in the official documentation`_.

If you're using MySQL_ with InnoDB_, it's practically the same situation.  The
data is laid out on disk in exactly the same way for both TEXT and VARCHAR
fields, as explained here_.  I couldn't find any resources about MyISAM other
than that TEXT is stored externally, but I just fired up a test table and did
some rudimentary benchmarking and the numbers were well within the margin of
error.

If you're using SQLite_, everything's a TEXT whether you want it to be or not (
with the notable exception of INTEGER PRIMARY KEY) so it doesn't matter what
you try to specify, it will be a TEXT.

I'm as guilty as anyone else on this--I use varchar all the time!  But come on,
let's stop imposing these arbitrary character limits on our columns when the
only reason we're doing it is for historical reasons.  Is anyone with me?  

.. _PostgreSQL: http://www.postgresql.org/
.. _`right here, in the official documentation`: http://www.postgresql.org/docs/8.3/interactive/datatype-character.html
.. _MySQL: http://www.mysql.com/
.. _InnoDB: http://www.innodb.com/
.. _SQLite: http://www.sqlite.org/
.. _here: http://forums.innodb.com/read.php?4,61,80#msg-80
.. _MSSQL: http://www.microsoft.com/sqlserver/2008/en/us/default.aspx