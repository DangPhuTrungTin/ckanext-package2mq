import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import pika
import constants 
from ckan.model import User
# import sqlalchemy.orm.scoping.scoped_session
import json
from time import gmtime, strftime
import logging


log = logging.getLogger(__name__)
def get_info(context,pkg_dict,type_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters\
        (constants.RABBITMQ_HOST,constants.RABBITMQ_PORT,'/',constants.credentials))        
    channel = connection.channel()
    channel.queue_declare(queue=constants.RABBITMQ_QUEUE)
    job_content= merge_two_dicts(get_useful_info_context(context), pkg_dict)
    job_content['action_type']=type_name
    channel.basic_publish(exchange='',
                    routing_key=constants.RABBITMQ_QUEUE,
                    body=json.dumps(job_content,default=str))
    connection.close()    
    return pkg_dict
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
def get_useful_info_context(context):
    content={}
    user= context['auth_user_obj']
    content['by_user_id']=user.id
    content['by_user_name']=user.display_name
    content['queried_at']=str(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    return content
class Package2MqPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController,inherit=True)
    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'package2mq')

    def after_create(self, context, pkg_dict):
        return get_info(context,pkg_dict,"create")
    def after_update(self, context, pkg_dict):
        return get_info(context,pkg_dict,"update")
    def after_delete(self, context, pkg_dict):
        return get_info(context,pkg_dict,"delete")