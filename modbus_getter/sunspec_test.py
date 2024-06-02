from SunSpec import *

def test_point_class():
    # Valid parameters
    try:
        point1 = Point("point1", "Label1", "Description1", point_type.pt_string, 1, "unit1", access_type.at_R, mandatory_type.mt_M, static_type.st_D)
        print("Point object created successfully with valid parameters.")
    except Exception as e:
        print("Error:", e)

    # Invalid parameters
    try:
        point2 = Point("123", "Label2", "Description2", point_type.pt_string, 1, "unit2", 7, mandatory_type.mt_M, static_type.st_D)
        print("Point object created successfully with invalid parameters.")
    except Exception as e:
        print("Error:", e)

    # Test getter and setter methods
    point3 = Point("point3", "Label3", "Description3", point_type.pt_string, 1, "unit3", access_type.at_R, mandatory_type.mt_M, static_type.st_D)
    point3.set_value("value3")
    assert point3.get_value() == "value3"
    print("Getter and setter methods tested successfully.")
    print(point3.to_json())

if __name__ == '__main__':
    # Run the test
    test_point_class()
