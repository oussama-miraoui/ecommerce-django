# Generated by Django 3.2.2 on 2021-07-06 23:55

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_client', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('adress', models.TextField(blank=True)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('methode_paiment', models.CharField(blank=True, max_length=20, null=True)),
                ('etat', models.CharField(choices=[('Trait??e', 'trait??e'), ('Non trait??e', 'Non trait??e')], default='Non trait??e', max_length=50)),
                ('Total', models.FloatField(null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.client')),
            ],
        ),
        migrations.CreateModel(
            name='Couleur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couleur', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Taille',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taille', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='images')),
                ('ancienPrix', models.PositiveIntegerField(blank=True, null=True)),
                ('prix', models.PositiveIntegerField()),
                ('stock', models.IntegerField()),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couleur', models.CharField(blank=True, max_length=50, null=True)),
                ('taille', models.CharField(blank=True, max_length=40, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('subtotal', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.client')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.produit')),
            ],
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(max_length=50)),
                ('montant', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.client')),
            ],
        ),
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Qte', models.PositiveBigIntegerField()),
                ('Commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.commande')),
                ('Produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.produit')),
            ],
        ),
        migrations.CreateModel(
            name='Detail_Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couleur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.couleur')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.produit')),
                ('taille', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.taille')),
            ],
        ),
        migrations.AddField(
            model_name='commande',
            name='paiement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.paiement'),
        ),
    ]
