# Api čerpání z jiných stránek
- mohu omezit pocet dotazu na Api 
- vysledek dotazu API uložím do databáze 
  - podle potřeby přímo k uživateli do tabulkz Profil
  - pro celou stranku s podmínkami jak často se mají aktualiyovat data


# Api poskytování dat jiným stránkám 
- Instalace nové aplikace 
```bash
python manage.py startapp api
```
instalace nove knihovny 
```bash
pip install djangorestframework
```

- nepotřebujeme forms.py 
- potřebujeme **serializers**
  - obdoba formuláře
  - **mixins** umožnují zobrazovat sezman 
  - **generic** 
  - urls.py -> definuji cestu k filmům 


# Mobilni aplikace pomocí API
- když chci ke stránce přidat aplikaci používám API 


## API permisions
- settings.py -> REST_FRAMEWORK 
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ]
}
```
  - recikluji permisions z Django accounts 
  - 
# Postman 
- 