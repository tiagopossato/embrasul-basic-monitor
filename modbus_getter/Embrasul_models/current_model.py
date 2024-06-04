from SunSpec import Model, PointGroup, Point, point_type

current_model = Model(id=3, start_address=74, update_interval=10,
    group = PointGroup(id="1", name="Corrente", label="Valores de corrente", 
    points = [
        Point(id='IrmsA', size=2, label='Corrente A', description='Corrente na fase A',  pt_type=point_type.float32, units="A"),
        Point(id='IrmsB', size=2, label='Corrente B', description='Corrente na fase B',  pt_type=point_type.float32, units="A"),
        Point(id='IrmsC', size=2, label='Corrente C', description='Corrente na fase C',  pt_type=point_type.float32, units="A"),
    ]))