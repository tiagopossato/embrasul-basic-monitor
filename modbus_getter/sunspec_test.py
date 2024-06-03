from SunSpec import *

def tepoint_class():
    # Valid parameters

    point1 = Point("point1", "MjC_", "Label1", "Description1", point_type.string, 1, "unit1", access_type.R, mandatory_type.M, static_type.D)
    point2 = Point("123", "VNT", "Label2", "Description2", point_type.string, 1, "unit2", access_type.RW, mandatory_type.M, static_type.D)
    inverter = PointGroup("7yj", "inverter", "inversor de frequdncia", "grupo de pontos do inversor de frequcnai", [
        point1, point2
    ])

    model = Model(307, inverter)

    point3 = Point("point1", "MjC_", "Label1", "Description1", point_type.string, 1, "unit1", access_type.R, mandatory_type.M, static_type.D)
    point4 = Point("123", "VNT", "Label2", "Description2", point_type.string, 1, "unit2", access_type.RW, mandatory_type.M, static_type.D)
    pgteste = PointGroup("7yj", "inverter", "inversor de frequdncia", "grupo de pontos do inversor de frequcnai", [
        point3, point4
    ])

    model2 = Model(45, pgteste)

    suns = SunSpec()
    suns.add_model(model)
    suns.add_model(model2)

    point1.set_value(34)

    point4.set_value("rere")
    
    print(suns.to_json())

if __name__ == '__main__':
    # Run the test
    tepoint_class()
