# Writing custom authentication backend
# import the User object
from django.contrib.auth.models import User
import ldap
#from .views import verifyLogin
#Note: I am using django provided User model but in real project create a custom model
class MyLdapAuth:
         # Create an authentication method
        # This is called by the standard Django login procedure
    def authenticate(self, request, username=None, password=None):
        print('inside authentication'+str(request.user.username))
       
        if MyLdapAuth.verifyLogin(username, password) != 'success':
            try:
                user = User.objects.get(username=username)
                #user.last_login=
                print('userName is: '+user.username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                list=username.split('.')
                user = User(username=username,first_name=list[0],last_name=list[1],email=username+str('@softvision.com'))
                #user.is_staff = True
                #user.is_superuser = True
                user.save()
                print('saved user username: '+User.objects.get(username=username).username)
            return user
        '''if request.path =='/admin':
            print('userAdmin::'+str(username))
            user = User(username=username)'''

        return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            print('comming here')
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None 

    # Writing my own logic for ldap authentication
    def  verifyLogin(username, password):  
       """Verifies credentials for username and password.
        Returns None on success or a string describing the error on failure
        # Adapt to your needs
        """
       LDAP_SERVER = 'your ldap server'
       # fully qualified AD user name
       LDAP_USERNAME = '%s@spi.com' % username
       # your password
       LDAP_PASSWORD = password
       base_dn = 'DC=spi,DC=com'
       ldap_filter = 'userPrincipalName=%s@spi.com' % username
       attrs = ['memberOf']
       try:
           # build a client
           ldap_client = ldap.initialize(LDAP_SERVER)
           # perform a synchronous bind
           ldap_client.set_option(ldap.OPT_REFERRALS,0)
           ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
       except ldap.INVALID_CREDENTIALS:
           #print("wron")
           ldap_client.unbind()
           return 'Wrong username or password'
       except ldap.SERVER_DOWN:
          #print("down")
          return 'AD server not awailable'
          # all is well
          # get all user groups and store it in cerrypy session for future use
          ab = str(ldap_client.search_s(base_dn,
                   ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf'])
          #print("ab"+ab)			   
       ldap_client.unbind()
       return 'success'       

#Later will use generic views to reduce the code    


    
    