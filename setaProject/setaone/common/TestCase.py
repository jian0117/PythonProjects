import time

class TestCase:
    case_name = 'demo'
    case_id = 0
    case_moudle = 'prom-admin'
    case_environment = 'dev'
    test_app = 'prom-admin'
    def __init__(self, case_environment):
        self.case_name = 'case_name'
        self.case_id = 0
        self.case_name_list = []
        self.case_environment = case_environment

    def add_case(self, case_name):
        self.case_id += 1
        add_result = self.case_name_list.append((self.case_id, case_name))
        return add_result


    def return_case_id_by_name(self, target_name):
        for case_id,case_name in self.case_name_list:
            if target_name == case_name:
                return case_id
        return None

if __name__ =='__main__':
    a_case = TestCase(case_environment='dev')
    case_name = 'test_001'
    a_case.add_case(case_name)
    time.sleep(1)
    print(a_case.return_case_id_by_name(case_name))