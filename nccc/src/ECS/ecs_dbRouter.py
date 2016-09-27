class ECSdbRouter(object):
    """A router to control all database operations on models in
    the myapp application"""

    def db_for_read(self, model, **hints):
        "Point all operations on myapp models to 'dbecs'"
        if model._meta.app_label == 'ECS':
            return 'dbecs'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on myapp models to 'dbecs'"
        if model._meta.app_label == 'ECS':
            return 'dbecs'
        return None


    #DISABLED MURAG WALA NA MANI
    '''
    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'myapp' or obj2._meta.app_label == 'myapp':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the myapp app only appears on the 'other' db"
        if db == 'other':
            return model._meta.app_label == 'myapp'
        elif model._meta.app_label == 'myapp':
            return False
        return None
    '''