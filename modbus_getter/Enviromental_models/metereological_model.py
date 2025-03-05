from SunSpec import Model, PointGroup, Point, point_type, RegisterType

metereological_model = Model(id=307, start_address=0, update_interval=30,register_type=RegisterType.INPUT_REGISTER,
    group = PointGroup(id="307", name="base_met", label="Base Met", 
    points = [
        Point(id='TmpAmb', size=2, label='Ambient Temperature', description='Temperatura ambiente',  pt_type=point_type.float32, units="C"),
        Point(id='RH', size=2, label='Relative Humidity', description='Umidade relativa',  pt_type=point_type.float32, units="%rh")
    ]))