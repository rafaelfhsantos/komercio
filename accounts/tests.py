from django.test import TestCase
from products.models import Product
from accounts.models import Account
from django.db.models.fields import UUIDField


from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.authtoken.models import Token

class AccountTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):        
        cls.user = Account.objects.create(
            username="seller_testing", 
            password="abcd",
            first_name="seller",
            last_name="testing",
            is_seller=True
        )        
   

    def test_id_is_uuid_not_editable_pk(self):
        user_id_type = type(self.user._meta.get_field('id'))
        self.assertEquals(user_id_type, UUIDField)

        user_id_is_pk = self.user._meta.get_field('id').primary_key
        self.assertEquals(user_id_is_pk, True)

        user_id_is_editable = self.user._meta.get_field('id').editable
        self.assertEquals(user_id_is_editable, False)


    def test_username_max_length_and_is_unique(self):        
        username_max_length = self.user._meta.get_field('username').max_length
        self.assertEquals(username_max_length, 50)

        username_is_unique = self.user._meta.get_field('username').unique
        self.assertEquals(username_is_unique, True)


    def test_first_name_max_length(self):        
        first_name_max_length = self.user._meta.get_field('first_name').max_length
        self.assertEquals(first_name_max_length, 50)


    def test_last_name_max_length(self):        
        last_name_max_length = self.user._meta.get_field('last_name').max_length
        self.assertEquals(last_name_max_length, 50)


    def test_is_seller_default_false(self):        
        is_seller_default = self.user._meta.get_field('is_seller').default
        self.assertEquals(is_seller_default, False)


class AccountViewsTest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.super_user = Account.objects.create_superuser(
            username='super_user', 
            password='1234abcd',
            first_name="Super",
            last_name= "UserSuper"        
        )
        cls.super_token = Token.objects.create(user=cls.super_user)

        cls.seller_user = Account.objects.create_user(
            username='seller_user', 
            password='abcd',
            first_name="Seller",
            last_name="UserSeller",
            is_seller=True        
        )
        cls.seller_token = Token.objects.create(user=cls.seller_user)

        cls.active_not_user = Account.objects.create_user(
            username='active_not_user', 
            password='abcd',
            first_name="Active or Not",
            last_name="Active User",
            is_seller=False        
        )


    

    def test_seller_creation(self):
        seller_data ={
            "username": "seller_view_tester",
            "password": "abcd",
            "first_name": "Seller View",
            "last_name": "Tester",
            "is_seller": True
        }

        response = self.client.post('/api/accounts/', seller_data)

        # import ipdb; ipdb.set_trace()

        seller_data_to_compare ={
            "username": "seller_view_tester",            
            "first_name": "Seller View",
            "last_name": "Tester",
            "is_seller": True
        }

        response_data_expected = {
            "username": response.data['username'],            
            "first_name": response.data['first_name'],
            "last_name": response.data['last_name'],
            "is_seller": response.data['is_seller']
        }
       

        self.assertEqual(response.status_code, 201)
        
        self.assertEqual(seller_data_to_compare, response_data_expected)


    def test_not_seller_creation(self):
        seller_data ={
            "username": "not_seller_view_tester",
            "password": "abcd",
            "first_name": "Not Seller View",
            "last_name": "Tester",
            "is_seller": False
        }

        response = self.client.post('/api/accounts/', seller_data)

        self.assertEqual(response.status_code, 201)
        
        self.assertEqual(False, response.data['is_seller'])

    
    def test_wrong_keys_seller_creation(self):        

        response = self.client.post('/api/accounts/', {})

        self.assertEqual(response.status_code, 400)

        response_data_expected = {
            'username': [ErrorDetail(string='This field is required.', code='required')], 
            'password': [ErrorDetail(string='This field is required.', code='required')], 
            'first_name': [ErrorDetail(string='This field is required.', code='required')], 
            'last_name': [ErrorDetail(string='This field is required.', code='required')]
        }        
        
        self.assertEqual(response_data_expected, response.data)

    
    def test_seller_login_returning_token(self):  
        seller_data ={
            "username": "seller_login_tester",
            "password": "abcd",
            "first_name": "Seller View",
            "last_name": "Tester",
            "is_seller": True
        }

        self.client.post('/api/accounts/', seller_data)

        response = self.client.post('/api/login/', {
            'username': 'seller_login_tester',
            'password': 'abcd'
        })

        # import ipdb; ipdb.set_trace()

        self.assertEqual(response.status_code, 200)
        
        self.assertTrue('token' in response.data )


    def test_seller_login_returning_token(self):      

        response = self.client.post('/api/login/', {
            'username': 'wrong_username',
            'password': 'abcd'
        })

        self.assertEqual(response.status_code, 400)

        expected_response ={'non_field_errors': [ErrorDetail(string='Unable to log in with provided credentials.', code='authorization')]}
        
        self.assertEqual(response.data, expected_response)    


    def test_only_account_owner_can_updade_his_account_info(self):          
        seller_owner_data ={
            "username": "seller_owner",
            "password": "abcd",
            "first_name": "Seller Owner",
            "last_name": "Tester",
            "is_seller": True
        }

        response_owner = self.client.post('/api/accounts/', seller_owner_data)

        seller_not_owner_data ={
            "username": "seller_not_owner",
            "password": "abcd",
            "first_name": "Seller Not Owner",
            "last_name": "Tester",
            "is_seller": True
        }

        self.client.post('/api/accounts/', seller_not_owner_data)

        response_login_owner = self.client.post('/api/login/', {
            'username': 'seller_owner',
            'password': 'abcd'
        })


        owner_token = response_login_owner.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + owner_token)

        owner_id = response_owner.data['id']

        response_update_owner = self.client.patch(f'/api/accounts/{owner_id}/', {
            'first_name': 'owner patched'
        })

        # import ipdb; ipdb.set_trace()

        self.assertEqual(response_update_owner.status_code, 200)
        self.assertEqual(response_update_owner.data['first_name'], 'owner patched')

        
        response_login_not_owner = self.client.post('/api/login/', {
            'username': 'seller_not_owner',
            'password': 'abcd'
        })

        not_owner_token = response_login_not_owner.data['token']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + not_owner_token)

        response_update_not_owner = self.client.patch(f'/api/accounts/{owner_id}/', {
            'first_name': 'owner patched again?'
        })

        self.assertEqual(response_update_not_owner.status_code, 403)


    def test_only_adm_can_deactivate_accounts(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)

        response_deactivate_not_adm = self.client.patch(f'/api/accounts/{self.seller_user.id}/management/', {
            'is_active': False
        })        

        self.assertEqual(response_deactivate_not_adm.status_code, 403)


        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)

        response_deactivate_adm = self.client.patch(f'/api/accounts/{self.seller_user.id}/management/', {
            'is_active': False
        })

        self.assertEqual(response_deactivate_adm.status_code, 200)


    def test_only_adm_can_reactivate_accounts(self):    

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)

        response_deactivate_adm = self.client.patch(f'/api/accounts/{self.active_not_user.id}/management/', {
            'is_active': False
        })

        self.assertEqual(response_deactivate_adm.status_code, 200)


        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)

        response_reactivate_not_adm = self.client.patch(f'/api/accounts/{self.active_not_user.id}/management/', {
            'is_active': True
        })                 

        self.assertEqual(response_reactivate_not_adm.status_code, 403)


        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)

        response_reactivate_adm = self.client.patch(f'/api/accounts/{self.active_not_user.id}/management/', {
            'is_active': True
        })

        self.assertEqual(response_reactivate_adm.status_code, 200)

    def test_anyone_can_list_users(self):
        response = self.client.get('/api/accounts/')

        self.assertEqual(response.status_code, 200)





    




        
