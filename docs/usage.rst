.. _usage:

Usage
=====

At the top of your base template add::

    {% load intercom_tags %}


And just before the ``</body>`` tag add::

    {% intercom_js user %}


And if you want a feedback/support link, put::

    <a id="Intercom" href="#">Support</a>

somewhere (e.g. in your nav bar) as explained by the **intercom.io** documentation.

In your settings file set ``INTERCOM_APP_ID`` and optionally (if you use a user hash for security) ``INTERCOM_USER_HASH_KEY`` with the values
provided by **intercom.io**.


Custom Data
-----------

**intercom.io** lets you send custom, per-user data to its site. **django-intercom** lets individual apps contribute what custom data they want to provide.

If you have an ``INTERCOM_APPS`` setting, it should be a list of apps that have an ``intercom`` module in them containing a ``custom_data`` function. This function should take a ``user`` and return a dictionary to be sent to **intercom.io** as custom data.

For example, if you have an app called ``foo`` with a ``Foo`` model, you might add::

    INTERCOM_APPS = [
        "foo",
    ]

to your settings and then in ``foo/intercom.py`` have::

    from foo.models import Foo
    
    def custom_data(user):
        return {
            "foo_count" : Foo.objects.filter(user=user).count(),
        }
