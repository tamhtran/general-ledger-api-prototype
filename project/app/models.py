from tortoise import fields, models


class Region(models.Model):
    region_id = fields.IntField(pk=True)
    name = fields.TextField()
    countries = fields.ReverseRelation["Country"]

    class Meta:
        table = "regions"


class Country(models.Model):
    country_id = fields.IntField(pk=True)
    name = fields.TextField()
    region_id = fields.ForeignKeyField('models.Region', related_name='countries', to_field='region_id')
    transactions = fields.ReverseRelation["Transaction"]

    class Meta:
        table = "countries"


class Account(models.Model):
    account_id = fields.IntField(pk=True)
    report = fields.TextField()
    class_ = fields.TextField(column_name='class')  # 'class' is a reserved keyword in Python
    subclass = fields.TextField()
    subclass2 = fields.TextField()
    account = fields.TextField()
    sub_account = fields.TextField()

    transactions = fields.ReverseRelation["Transaction"]

    class Meta:
        table = "accounts"


class Transaction(models.Model):
    transaction_id = fields.IntField(pk=True)  # Primary key as an integer
    entry_no = fields.TextField(null=False)
    date = fields.DateField(null=False)
    country_id = fields.ForeignKeyField('models.Country', related_name='transactions', to_field='country_id', null=False)
    account_id = fields.ForeignKeyField('models.Account', related_name='transactions', to_field='account_id', null=False)
    details = fields.TextField(null=False)
    amount = fields.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        table = "transactions"



