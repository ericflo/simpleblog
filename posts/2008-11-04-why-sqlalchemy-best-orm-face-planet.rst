---
layout: post
title: "Why SQLAlchemy is the best ORM on the face of the planet"
date: 2008-11-04T20:03:04-06:00
comments: false
categories: [Python, SQLAlchemy]
published: true
alias: [/blog/post/why-sqlalchemy-best-orm-face-planet]
---

SQLAlchemy_ started out with a bang.  When it came out, there was really nothing else out there that even came close in terms of features, performance, and ease of use.  SQLObject_ was the reigning champion of Python ORMs, and the Django ORM was around but much less powerful at that time.  So now it's 3 years later.  Is SQLAlchemy still the best?  I think it is, and here's why:

1.  It has *no* preconception of how your database should be laid out.  If you haven't created your database yet, you can choose to use the ActiveRecord-style layout of one object mapping to one table.  If that's not the case for your application, you can even map arbitrary select statements onto objects, if that's how much flexibility you want.  So already, SQLAlchemy is an option for thousands of people for which the other ORMs would not be.

2.  It's tuned for performance.  Whether it's the extremely slick connection pooling feature, or whether it's the `Unit of Work`_ design pattern which will issue as few queries as possible.  Whether it's the ability to specify lazily or eagerly loaded columns, or whether you note the identity map which keeps track of all of the objects that are in memory, SQLAlchemy has lots of performance-tuning abilities.  In my mind, SQLAlchemy gives you all the tools that you need to create a blazing fast application.

3. It has a wonderful community which is building great tools on top of SQLAlchemy itself.  A clear example of this is the set of plugins that are shipped with SQLAlchemy, by default.  These include a simple declarative_ layer, an `association proxy`_, and SqlSoup_, which uses introspection to map tables on the fly.  These are great examples of how the community is creating great libraries that sit on top of SQLAlchemy.  They also serve as proof of the configurability of the ORM itself.

4. It supports your database.  According to its own website, "SQLAlchemy includes dialects for SQLite, Postgres, MySQL, Oracle, MS-SQL, Firebird, MaxDB, MS Access, Sybase and Informix; IBM has also released a DB2 driver."  This is a pretty massive list and goes a long way in proving the power of the ORM.

It comes down to this.  SQLAlchemy is a well-designed, performant, widely supported ORM which treats SQL with the respect it deserves.  I haven't provided any code samples here because you should do that yourselves, with your own apps.  It's just that good.  So what are you waiting for?

.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _SQLObject: http://www.sqlobject.org/
.. _`Unit of Work`: http://www.sqlalchemy.org/docs/05/session.html#unitofwork
.. _declarative: http://www.sqlalchemy.org/docs/05/plugins.html#plugins_declarative
.. _`association proxy`: http://www.sqlalchemy.org/docs/05/plugins.html#plugins_associationproxy
.. _SqlSoup: http://www.sqlalchemy.org/docs/05/plugins.html#plugins_sqlsoup