import datetime

from airflow import DAG
from airflow.operators import bash_operator
from airflow.operators import python_operator
from airflow.operators import dummy_operator

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    'start_date': datetime.datetime(2023, 8, 25),
    'email': ['2dee79d649-52f9f5+1@inbox.mailtrap.io'],
    'email_on_failure': True
}

with DAG(
        'running_python_bash_and_dummy_operator_failed',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

    def hello_world():
        print('Hello World!')
        return 1

    def greeting():
        print('Greetings from SpikeySales! Happy shopping.')
        raise TypeError("Sorry, only strings are allowed")
        return 'Greeting successfully printed.'

    hello_world_greeting = python_operator.PythonOperator(
        task_id='python_1',
        python_callable=hello_world)
    

    spikeysales_greeting = python_operator.PythonOperator(
        task_id='python_2',
        python_callable=greeting)

    bash_greeting = bash_operator.BashOperator(
        task_id='bye_bash',
        bash_command='echo Goodbye! Hope to see you soon.')

    end = dummy_operator.DummyOperator(
        task_id='dummy')

    hello_world_greeting >> spikeysales_greeting >> bash_greeting >> end