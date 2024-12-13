import os
import sys
import django

# Configura Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import transaction
from django.core.management import call_command
from accounts.models import UserModel, StudentModel, ProviderModel
from inventory.models import LocationModel, ProductModel, CategoryModel  # Asegúrate de importar esto
from inventory.factories import (
    WarehouseFactory, LocationFactory, ProductFactory, 
    InventoryFactory, InventoryTransactionFactory
)
from accounts.choices import DegreeChoices, RoleChoices
from inventory.choices import MovementChoices, TypeChoices
from faker import Faker
from faker.exceptions import UniquenessException

fake = Faker()

# Borra todos los datos de la base de datos
def clear_database():
    call_command('flush', '--no-input')

# Crea roles
def create_roles():
    admin_role = RoleChoices.ADMIN
    employee_role = RoleChoices.EMPLOYEE
    viewer_role = RoleChoices.VIEWER
    return admin_role, employee_role, viewer_role

# Crea usuarios
def create_users():
    admin_role, employee_role, viewer_role = create_roles()
    # Crear superusuario
    superuser = UserModel.objects.create_superuser(
        email='admin@gmail.com',
        first_name='Admin',
        last_name='Admin',
        password='123'
    )
    superuser.role = admin_role
    superuser.save()

    # Crear usuario normal
    user = UserModel.objects.create_user(
        email='yael@example.com',
        first_name='Yael',
        last_name='González',
        password='brilliant24'
    )
    user.role = employee_role
    user.save()

    user = UserModel.objects.create_user(
        email='viewer@example.com',
        first_name='Viewer',
        last_name='User',
        password='brilliant24'
    )
    user.role = viewer_role
    user.save()

    # Crear 2 administradores adicionales
    for i in range(2):
        admin = UserModel.objects.create_user(
            email=f'admin{i}@example.com',
            first_name=f'Admin{i}',
            last_name=f'User{i}',
            password=f'adminpass{i}'
        )
        admin.role = admin_role
        admin.save()

    # Crear 2 empleados adicionales
    for i in range(2):
        employee = UserModel.objects.create_user(
            email=f'employee{i}@example.com',
            first_name=f'Employee{i}',
            last_name=f'User{i}',
            password=f'employeepass{i}'
        )
        employee.role = employee_role
        employee.save()

# Crea usuarios adicionales
def create_additional_users():
    additional_users = [
        {"clave": "ARIAS JUAREZ JOEL", "password": "199"},
        {"clave": "CORTEZ GALVAN PABLO ALBERTO", "password": "2794"},
        {"clave": "DOMINGUEZ REYES JULIO", "password": "297"},
        {"clave": "FELIX GARCIA JORGE GUADALUPE", "password": "446"},
        {"clave": "IBARRA AHUMADA CRISTOBAL", "password": "478"},
        {"clave": "LARES RAMIREZ ISMAEL", "password": "510"},
        {"clave": "LOAEZA MORENO RONI", "password": "554"},
        {"clave": "MAGDALENO PALENCIA MA. ANGELICA", "password": "586"},
        {"clave": "MENDOZA MARMOLEJO JUAN ALBERTO", "password": "623"},
        {"clave": "MORENO PIZANO JESUS", "password": "608"},
        {"clave": "MORONES GARCIA AURELIO", "password": "635"},
        {"clave": "MUÑOZ SALAZAR LUIS FELIPE", "password": "645"},
        {"clave": "NICOLAS DE LA ROSA NOE", "password": "644"},
        {"clave": "NICOLAS HERNANDEZ JOSE ELOY ENRIQUE", "password": "646"},
        {"clave": "NICOLAS SANCHEZ JOSE EPIFANIO RUFINO", "password": "652"},
        {"clave": "ORNELAS URIBE ENRIQUE MARCO", "password": "680"},
        {"clave": "PADUA HERNANDEZ AGUSTIN", "password": "2959"},
        {"clave": "PATIÑO GONZALEZ HUMBERTO", "password": "768"},
        {"clave": "RICO MEZA ALFONSO", "password": "2074"},
        {"clave": "RODRIGUEZ ACEVEDO ALEJANDRO", "password": "811"},
        {"clave": "ROJAS SANCHEZ CLARA", "password": "783"},
        {"clave": "ROMERO CRUZ JOSE RAMON", "password": "2679"},
        {"clave": "SANCHEZ PEREZ JOSE ANTONIO", "password": "887"},
        {"clave": "SOTO NIEBLAS JUAN JOSE", "password": "199"},
    ]

    _, employee_role, _ = create_roles()

    for user in additional_users:
        full_name = user["clave"]
        password = user["password"]
        names = full_name.split()
        last_name = names[-2] if len(names) > 2 else names[-1]
        first_name = names[0]
        email = f"{last_name.lower()}{first_name[0].lower()}@tectijuana.edu.mx"

        created_user = UserModel.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        created_user.role = employee_role
        created_user.save()

# Crea almacenes y ubicaciones
def create_warehouses_and_locations():
    warehouses = []
    for name in ['Otay', 'Tomás Aquino']:
        warehouse = WarehouseFactory(name=name)
        warehouses.append(warehouse)
        for _ in range(15):  # Crear 15 ubicaciones por almacén
            try:
                LocationFactory(warehouse=warehouse)
            except UniquenessException:
                pass  # Si se alcanza el límite de intentos, simplemente ignora la excepción
    print(f"Created {len(warehouses)} warehouses and {len(warehouses[0].locations.all())} locations per warehouse.")

# Crea categorías
def create_categories():
    categories = [
        (21101, "MATERIALES Y ÚTILES DE OFICINA"),
        (21201, "MATERIALES Y ÚTILES DE IMPRESIÓN Y REPRODUCCIÓN"),
        (21301, "MATERIAL ESTADÍSTICO Y GEOGRÁFICO"),
        (21401, "MATERIALES Y ÚTILES CONSUMIBLES PARA EL PROCESAMIENTO EN EQUIPOS Y BIENES INFORMÁTICOS"),
        (21501, "MATERIAL DE APOYO INFORMATIVO"),
        (21502, "MATERIAL PARA INFORMACIÓN EN ACTIVIDADES DE INVESTIGACIÓN CIENTÍFICA Y TECNOLÓGICA"),
        (21601, "MATERIAL DE LIMPIEZA"),
        (22103, "PRODUCTOS ALIMENTICIOS PARA EL PERSONAL QUE REALIZA LABORES EN CAMPO O DE SUPERVISION"),
        (22104, "PRODUCTOS ALIMENTICIOS PARA EL PERSONAL EN LAS INSTALACIONES DE LAS DEPENDENCIAS Y ENTIDADES"),
        (22201, "PRODUCTOS ALIMENTICIOS PARA ANIMALES"),
        (22301, "UTENSILIOS PARA EL SERVICIO DE ALIMENTACIÓN"),
        (23101, "PRODUCTOS ALIMENTICIOS, AGROPECUARIOS Y FORESTALES ADQUIRIDOS COMO MATERIA PRIMA"),
        (24101, "PRODUCTOS MINERALES NO METÁLICOS"),
        (24201, "CEMENTO Y PRODUCTOS DE CONCRETO"),
        (24301, "CAL, YESO Y PRODUCTOS DE YESO"),
        (24401, "MADERA Y PRODUCTOS DE MADERA"),
        (24501, "VIDRIO Y PRODUCTOS DE VIDRIO"),
        (24601, "MATERIAL ELÉCTRICO Y ELECTRÓNICO"),
        (24701, "ARTÍCULOS METÁLICOS PARA LA CONSTRUCCIÓN"),
        (24801, "MATERIALES COMPLEMENTARIOS"),
        (24901, "OTROS MATERIALES Y ARTÍCULOS DE CONSTRUCCIÓN Y REPARACIÓN"),
        (25101, "PRODUCTOS QUÍMICOS BÁSICOS"),
        (25201, "PLAGUICIDAS, ABONOS Y FERTILIZANTES"),
        (25301, "MEDICINAS Y PRODUCTOS FARMACÉUTICOS"),
        (25401, "MATERIALES, ACCESORIOS Y SUMINISTROS MÉDICOS."),
        (25501, "MATERIALES, ACCESORIOS Y SUMINISTROS DE LABORATORIO"),
        (25601, "FIBRAS SINTÉTICAS, HULES, PLÁSTICOS Y DERIVADOS"),
        (25901, "OTROS PRODUCTOS QUÍMICOS"),
        (26102, "COMBUSTIBLES, LUBRICANTES Y ADITIVOS PARA VEHÍCULOS TERRESTRES, AÉREOS, MARÍTIMOS, LACUSTRES Y FLUVIALES DESTINADOS A SERVICIOS PÚBLICOS Y LA OPERACIÓN DE PROGRAMAS PÚBLICOS"),
        (26103, "COMBUSTIBLES, LUBRICANTES Y ADITIVOS PARA VEHÍCULOS TERRESTRES, AÉREOS, MARÍTIMOS, LACUSTRES Y FLUVIALES DESTINADOS A SERVICIOS ADMINISTRATIVOS"),
        (26104, "COMBUSTIBLES, LUBRICANTES Y ADITIVOS PARA VEHÍCULOS TERRESTRES, AÉREOS, MARÍTIMOS, LACUSTRES Y FLUVIALES ASIGNADOS A SERVIDORES PÚBLICOS"),
        (26105, "COMBUSTIBLES, LUBRICANTES Y ADITIVOS PARA MAQUINARIA, EQUIPO DE PRODUCCIÓN Y SERVICIOS ADMINISTRATIVOS"),
        (27101, "VESTUARIO Y UNIFORMES"),
        (27201, "PRENDAS DE PROTECCIÓN PERSONAL"),
        (27301, "ARTÍCULOS DEPORTIVOS"),
        (27401, "PRODUCTOS TEXTILES"),
        (27501, "BLANCOS Y OTROS PRODUCTOS TEXTILES, EXCEPTO PRENDAS DE VESTIR"),
        (29101, "HERRAMIENTAS MENORES"),
        (29201, "REFACCIONES Y ACCESORIOS MENORES DE EDIFICIOS"),
        (29301, "REFACCIONES Y ACCESORIOS MENORES DE MOBILIARIO Y EQUIPO DE ADMINISTRACIÓN, EDUCACIONAL Y RECREATIVO"),
        (29401, "REFACCIONES Y ACCESORIOS PARA EQUIPO DE CÓMPUTO Y TELECOMUNICACIONES"),
        (29501, "REFACCIONES Y ACCESORIOS MENORES DE EQUIPO E INSTRUMENTAL MEDICO Y DE LABORATORIO"),
        (29601, "REFACCIONES Y ACCESORIOS MENORES DE EQUIPO DE TRANSPORTE"),
        (29801, "REFACCIONES Y ACCESORIOS MENORES DE MAQUINARIA Y OTROS EQUIPOS"),
        (29901, "REFACCIONES Y ACCESORIOS MENORES OTROS BIENES MUEBLES"),
        (31101, "SERVICIO DE ENERGÍA ELÉCTRICA"),
        (31201, "SERVICIO DE GAS"),
        (31301, "SERVICIO DE AGUA"),
        (31401, "SERVICIO TELEFÓNICO CONVENCIONAL"),
        (31601, "SERVICIO DE RADIOLOCALIZACIÓN"),
        (31602, "SERVICIOS DE TELECOMUNICACIONES"),
        (31603, "SERVICIOS DE INTERNET"),
        (31701, "SERVICIOS DE CONDUCCIÓN DE SEÑALES ANALÓGICAS Y DIGITALES"),
        (31801, "SERVICIO POSTAL"),
        (31802, "SERVICIO TELEGRÁFICO"),
        (31901, "SERVICIOS INTEGRALES DE TELECOMUNICACIÓN"),
        (31904, "SERVICIOS INTEGRALES DE INFRAESTRUCTURA DE CÓMPUTO"),
        (32301, "ARRENDAMIENTO DE EQUIPO Y BIENES INFORMÁTICOS"),
        (32302, "ARRENDAMIENTO DE MOBILIARIO"),
        (32303, "ARRENDAMIENTO DE EQUIPO DE TELECOMUNICACIONES"),
        (32601, "ARRENDAMIENTO DE MAQUINARIA Y EQUIPO"),
        (32701, "PATENTES, DERECHOS DE AUTOR, REGALÍAS Y OTROS"),
        (32903, "OTROS ARRENDAMIENTOS"),
        (33301, "SERVICIOS DE DESARROLLO DE APLICACIONES INFORMÁTICAS"),
        (33303, "SERVICIOS RELACIONADOS CON CERTIFICACIÓN DE PROCESOS"),
        (33304, "SERVICIOS DE MANTENIMIENTO DE APLICACIONES INFORMÁTICAS"),
        (33401, "SERVICIOS PARA CAPACITACIÓN A SERVIDORES PÚBLICOS"),
        (33601, "SERVICIOS RELACIONADOS CON TRADUCCIONES"),
        (33602, "OTROS SERVICIOS COMERCIALES"),
        (33603, "IMPRESIONES DE DOCUMENTOS OFICIALES PARA LA PRESTACIÓN DE SERVICIOS PÚBLICOS, IDENTIFICACIÓN, FORMATOS ADMINISTRATIVOS Y FISCALES, FORMAS VALORADAS, CERTIFICADOS Y TÍTULOS"),
        (33604, "IMPRESIÓN Y ELABORACIÓN DE MATERIAL INFORMATIVO DERIVADO DE LA OPERACIÓN Y ADMINISTRACIÓN DE LAS DEPENDENCIAS Y ENTIDADES"),
        (33605, "INFORMACIÓN EN MEDIOS MASIVOS DERIVADA DE LA OPERACIÓN Y ADMINISTRACIÓN DE LAS DEPENDENCIAS Y ENTIDADES"),
        (33606, "SERVICIOS DE DIGITALIZACIÓN"),
        (33801, "SERVICIOS DE VIGILANCIA"),
        (33901, "SUBCONTRATACIÓN DE SERVICIOS CON TERCEROS"),
        (34101, "SERVICIOS BANCARIOS Y FINANCIEROS"),
        (34501, "SEGURO DE BIENES PATRIMONIALES"),
        (34601, "ALMACENAJE, EMBALAJE Y ENVASE"),
        (34701, "FLETES Y MANIOBRAS"),
        (34901, "SERVICIOS FINANCIEROS, BANCARIOS Y COMERCIALES INTEGRALES"),
        (35101, "MANTENIMIENTO Y CONSERVACIÓN DE INMUEBLES PARA LA PRESTACIÓN DE SERVICIOS ADMINISTRATIVOS"),
        (35102, "MANTENIMIENTO Y CONSERVACIÓN DE INMUEBLES PARA LA PRESTACIÓN DE SERVICIOS PÚBLICOS"),
        (35201, "MANTENIMIENTO Y CONSERVACIÓN DE MOBILIARIO Y EQUIPO DE ADMINISTRACIÓN"),
        (35301, "MANTENIMIENTO Y CONSERVACIÓN DE BIENES INFORMÁTICOS"),
        (35401, "INSTALACIÓN, REPARACIÓN Y MANTENIMIENTO DE EQUIPO E INSTRUMENTAL MEDICO Y DE LABORATORIO"),
        (35501, "MANTENIMIENTO Y CONSERVACIÓN DE VEHÍCULOS TERRESTRES, AÉREOS, MARÍTIMOS, LACUSTRES Y FLUVIALES"),
        (35701, "MANTENIMIENTO Y CONSERVACIÓN DE MAQUINARIA Y EQUIPO"),
        (35801, "SERVICIOS DE LAVANDERÍA, LIMPIEZA E HIGIENE"),
        (35901, "SERVICIOS DE JARDINERÍA Y FUMIGACIÓN"),
        (36101, "DIFUSIÓN DE MENSAJES SOBRE PROGRAMAS Y ACTIVIDADES GUBERNAMENTALES"),
        (37101, "PASAJES AÉREOS NACIONALES PARA LABORES EN CAMPO Y DE SUPERVISIÓN"),
        (37104, "PASAJES AÉREOS NACIONALES PARA SERVIDORES PÚBLICOS DE MANDO EN EL DESEMPEÑO DE COMISIONES Y FUNCIONES OFICIALES"),
        (37106, "PASAJES AÉREOS INTERNACIONALES PARA SERVIDORES PÚBLICOS EN EL DESEMPEÑO DE COMISIONES Y FUNCIONES OFICIALES"),
        (37201, "PASAJES TERRESTRES NACIONALES PARA LABORES EN CAMPO Y DE SUPERVISIÓN"),
        (37204, "PASAJES TERRESTRES NACIONALES PARA SERVIDORES PÚBLICOS DE MANDO EN EL DESEMPEÑO DE COMISIONES Y FUNCIONES OFICIALES"),
        (37206, "PASAJES TERRESTRES INTERNACIONALES PARA SERVIDORES PÚBLICOS EN EL DESEMPEÑO DE COMISIONES Y FUNCIONES OFICIALES"),
        (37207, "PASAJES TERRESTRES NACIONALES POR MEDIO ELECTRÓNICO"),
        (37301, "PASAJES MARÍTIMOS, LACUSTRES Y FLUVIALES PARA LABORES EN CAMPO Y SUPERVISIÓN"),
        (37304, "PASAJES MARÍTIMOS, LACUSTRES Y FLUVIALES PARA SERVIDORES PÚBLICOS DE MANDO EN EL DESEMPEÑO DE COMISIONES Y FUNCIONES OFICIALES"),
        (37501, "VIÁTICOS NACIONALES PARA LABORES EN CAMPO Y DE SUPERVISIÓN"),
        (37504, "VIÁTICOS NACIONALES PARA SERVIDORES PÚBLICOS EN EL DESEMPEÑO DE FUNCIONES OFICIALES"),
        (37602, "VIÁTICOS EN EL EXTRANJERO PARA SERVIDORES PÚBLICOS EN EL DESEMPEÑO DE COMISIONES Y FUNCIONES OFICIALES"),
        (37701, "INSTALACIÓN DEL PERSONAL FEDERAL"),
        (37801, "SERVICIOS INTEGRALES NACIONALES PARA SERVIDORES PÚBLICOS EN EL DESEMPEÑO DE COMISIONES Y FUNCIONES OFICIALES"),
        (37802, "SERVICIOS INTEGRALES EN EL EXTRANJERO PARA SERVIDORES PÚBLICOS EN EL DESEMPEÑO DE COMISIONES Y FUNCIONES OFICIALES"),
        (37901, "GASTOS PARA OPERATIVOS Y TRABAJOS DE CAMPO EN ÁREAS RURALES"),
        (38201, "GASTOS DE ORDEN SOCIAL"),
        (38301, "CONGRESOS Y CONVENCIONES"),
        (38401, "EXPOSICIONES"),
        (39201, "IMPUESTOS Y DERECHOS DE EXPORTACIÓN"),
        (39202, "OTROS IMPUESTOS Y DERECHOS"),
        (39301, "IMPUESTOS Y DERECHOS DE IMPORTACIÓN"),
        (39401, "EROGACIONES POR RESOLUCIONES POR AUTORIDAD COMPETENTE"),
        (39501, "PENAS, MULTAS, ACCESORIOS Y ACTUALIZACIONES"),
        (39601, "PÉRDIDAS DEL ERARIO FEDERAL"),
        (43901, "SUBSIDIOS PARA CAPACITACION Y BECAS"),
        (44101, "GASTOS RELACIONADOS CON ACTIVIDADES CULTURALES, DEPORTIVAS Y DE AYUDA EXTRAORDINARIA"),
        (44102, "GASTOS POR SERVICIOS DE TRASLADO DE PERSONAS"),
        (51101, "MOBILIARIO"),
        (51201, "MUEBLES, EXCEPTO DE OFICINA Y ESTANTERÍA"),
        (51301, "BIENES ARTÍSTICOS Y CULTURALES"),
        (51501, "BIENES INFORMÁTICOS"),
        (51901, "EQUIPO DE ADMINISTRACIÓN"),
        (52101, "EQUIPOS Y APARATOS AUDIOVISUALES"),
        (52201, "APARATOS DEPORTIVOS"),
        (52301, "CÁMARAS FOTOGRÁFICAS Y DE VIDEO"),
        (52901, "OTRO MOBILIARIO Y EQUIPO EDUCACIONAL Y RECREATIVO"),
        (53101, "EQUIPO MEDICO Y DE LABORATORIO"),
        (53201, "INSTRUMENTAL MEDICO Y DE LABORATORIO"),
        (54103, "VEHÍCULOS Y EQUIPO TERRESTRES DESTINADOS A SERVICIOS PÚBLICOS Y LA OPERACIÓN DE PROGRAMAS PÚBLICOS"),
        (54201, "CARROCERÍAS Y REMOLQUES"),
        (54901, "OTROS EQUIPOS DE TRANSPORTE"),
        (56101, "MAQUINARIA Y EQUIPO AGROPECUARIO"),
        (56201, "MAQUINARIA Y EQUIPO INDUSTRIAL"),
        (56401, "SISTEMAS DE AIRE ACONDICIONADO, CALEFACCIÓN Y DE REFRIGERACIÓN INDUSTRIAL Y COMERCIAL"),
        (56501, "EQUIPOS Y APARATOS DE COMUNICACIONES Y TELECOMUNICACIONES"),
        (56601, "MAQUINARIA Y EQUIPO ELÉCTRICO Y ELECTRÓNICO"),
        (56701, "HERRAMIENTAS Y MAQUINAS HERRAMIENTA"),
        (56902, "OTROS BIENES MUEBLES"),
        (57101, "ANIMALES DE REPRODUCCIÓN"),
        (57201, "PORCINOS"),
        (57301, "AVES"),
        (57401, "OVINOS Y CAPRINOS"),
        (57501, "PECES Y ACUICULTURA"),
        (57601, "ANIMALES DE TRABAJO"),
        (57701, "ANIMALES DE CUSTODIA Y VIGILANCIA"),
        (57801, "ARBOLES Y PLANTAS"),
        (57901, "OTROS ACTIVOS BIOLÓGICOS"),
        (59101, "SOFTWARE"),
        (59201, "PATENTES"),
        (59301, "MARCAS"),
        (59401, "DERECHOS"),
        (59701, "LICENCIAS INFORMÁTICAS E INTELECTUALES"),
        (59901, "OTROS ACTIVOS INTANGIBLES")
    ]

    categories_created = 0
    for code, name in categories:
        try:
            CategoryModel.objects.create(code=code, name=name)
            categories_created += 1
        except Exception as e:
            print(f"Error creating category {name}: {e}")
    
    print(f"Created {categories_created} categories.")

# Crea productos
def create_products():
    categories = list(CategoryModel.objects.all())
    products_created = 0
    for _ in range(800):  # Crear 800 productos
        try:
            product = ProductFactory(
                category=fake.random_element(elements=categories)
            )
            products_created += 1
        except UniquenessException:
            pass  # Si se alcanza el límite de intentos, simplemente ignora la excepción
    print(f"Created {products_created} products.")

# Crea personas (estudiantes y proveedores)
def create_persons():
    persons = []
    for _ in range(10):  # Crear 10 estudiantes
        student = StudentModel.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            control_number=fake.unique.bothify(text='????########'),
            degree=fake.random_element(elements=[choice[0] for choice in DegreeChoices.choices])
        )
        persons.append(student)

    for _ in range(10):  # Crear 10 proveedores
        provider = ProviderModel.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            RFC=fake.unique.bothify(text='???######???'),
            NSS=fake.unique.bothify(text='###########')
        )
        persons.append(provider)

    print(f"Created {len(persons)} persons (students and providers).")
    return persons

# Crea inventarios
def create_inventories():
    inventories = []
    products = ProductModel.objects.all()
    locations = LocationModel.objects.all()

    if not products.exists():
        print("No products available for creating inventories.")
        return inventories

    if not locations.exists():
        print("No locations available for creating inventories.")
        return inventories

    for _ in range(100):  # Crear 100 inventarios
        try:
            inventory = InventoryFactory(
                product=fake.random_element(products),
                location=fake.random_element(locations)
            )
            inventories.append(inventory)
        except UniquenessException as e:
            print(f"UniquenessException: {e}")
            pass  # Si se alcanza el límite de intentos, simplemente ignora la excepción
        except Exception as e:
            print(f"Exception: {e}")
            pass  # Captura cualquier otra excepción y la reporta

    print(f"Created {len(inventories)} inventories.")
    return inventories

# Crea transacciones de inventario
def create_inventory_transactions(persons, inventories):
    if not inventories:
        print("No inventories created.")
        return

    if not persons:
        print("No persons created.")
        return

    transactions_created = 0
    for _ in range(500):  # Crear 500 transacciones de inventario
        try:
            inventory = fake.random_element(inventories)
            movement = fake.random_element(elements=[MovementChoices.IN, MovementChoices.OUT])
            type_choice = fake.random_element(elements=[choice[0] for choice in TypeChoices.choices])
            
            # Validación de restricciones de tipo y movimiento
            if movement == MovementChoices.IN and type_choice in [TypeChoices.LOST, TypeChoices.DAMAGED, TypeChoices.LOAN, TypeChoices.SALE]:
                type_choice = fake.random_element(elements=[choice[0] for choice in TypeChoices.choices if choice not in [TypeChoices.LOST, TypeChoices.DAMAGED, TypeChoices.LOAN, TypeChoices.SALE]])
            if movement == MovementChoices.OUT and type_choice in [TypeChoices.PURCHASE, TypeChoices.RETURN]:
                type_choice = fake.random_element(elements=[choice[0] for choice in TypeChoices.choices if choice not in [TypeChoices.PURCHASE, TypeChoices.RETURN]])
            
            # Validación de cantidad
            quantity = fake.random_int(min=1, max=inventory.quantity if movement == MovementChoices.OUT and inventory.quantity > 0 else 100)
            
            InventoryTransactionFactory(
                inventory=inventory,
                person=fake.random_element(persons),
                quantity=quantity,
                movement=movement,
                type=type_choice,
                description=fake.text(max_nb_chars=128)
            )
            transactions_created += 1
        except ValueError:
            pass  # Si ocurre un ValueError (por ejemplo, por inventario insuficiente), simplemente ignora la excepción

    print(f"Created {transactions_created} inventory transactions.")

# Ejecuta el script
def populate_database():
    clear_database()
    create_users()
    create_additional_users()  # Llama a la nueva función para crear usuarios adicionales
    create_warehouses_and_locations()
    create_categories()
    create_products()

    # Crear personas y realizar transacciones
    persons = create_persons()
    inventories = create_inventories()

    if not inventories:
        print("Error: No inventories created.")
        return

    if not persons:
        print("Error: No persons created.")
        return

    create_inventory_transactions(persons, inventories)

if __name__ == '__main__':
    with transaction.atomic():
        populate_database()
