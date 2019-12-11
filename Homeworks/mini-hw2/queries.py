from __future__ import print_function

import vertica_python as vp
import time

'''
Here are the lines to move the data from local to ec2
scp -i /home/bdvr/DATA516/keys/BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Homeworks/mini-hw2/hidden.csv ubuntu@ec2-52-90-127-226.compute-1.amazonaws.com:~/
scp -i /home/bdvr/DATA516/keys/BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Homeworks/mini-hw2/stories.csv ubuntu@ec2-52-90-127-226.compute-1.amazonaws.com:~/
scp -i /home/bdvr/DATA516/keys/BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Homeworks/mini-hw2/taggings.csv ubuntu@ec2-52-90-127-226.compute-1.amazonaws.com:~/
scp -i /home/bdvr/DATA516/keys/BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Homeworks/mini-hw2/tags.csv ubuntu@ec2-52-90-127-226.compute-1.amazonaws.com:~/
scp -i /home/bdvr/DATA516/keys/BDVRDATA516KP.pem /home/bdvr/DATA516/avanroi1/Homeworks/mini-hw2/queries.py ubuntu@ec2-52-90-127-226.compute-1.amazonaws.com:~/

'''


args = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    # 10 minutes timeout on queries
    'read_timeout': 600,
    # default throw error on invalid UTF-8 results
    'unicode_error': 'strict',
    # SSL is disabled by default
    'ssl': False,
    # connection timeout is not enabled by default
    'connection_timeout': 5
}

with vp.connect(**args) as conn:
    cur = conn.cursor()

    # Create the tables
    createTables=False
    if(createTables==True):
        cur.execute("""
        CREATE SCHEMA lobsters;
        CREATE TABLE lobsters.tags ( id integer NOT NULL, tag varchar(64));

        CREATE TABLE lobsters.taggings (id integer NOT NULL, story_id integer NOT NULL, tag_id integer NOT NULL);

        CREATE TABLE lobsters.hiddens (id integer NOT NULL, user_id integer NOT NULL, story_id integer NOT NULL);

        CREATE TABLE lobsters.stories (
        id integer NOT NULL,
        created_at TIMESTAMP,
        description varchar(4095),
        hotness float,
        markeddown_description varchar(4095),
        short_id varchar(255),
        title varchar(1023),
        upvotes integer,
        downvotes integer,
        url varchar(255),
        user_id integer);
        """)

        with open("taggings.csv", "rb") as f:
            cur.copy("COPY lobsters.taggings from stdin DELIMITER ','", f)

        with open("hidden.csv", "rb") as f:
            cur.copy("COPY lobsters.hiddens from stdin DELIMITER ','", f)

        with open("stories.csv", "rb") as f:
            cur.copy("COPY lobsters.stories from stdin DELIMITER ','", f)
    introQueries = False
    if(introQueries):
        # Execute some query
        cur.execute("""
        select * from lobsters.stories where user_id=1;
        """)
        print(cur.fetchall())

        cur.execute("""
        select count(*) from lobsters.stories where user_id = 1;
        """)
        print(cur.fetchall())

    queryA=True
    if(queryA):
        cur.execute("""
        Select title,hotness from lobsters.stories order by hotness desc LIMIT 10;
        """)
        print(cur.fetchall())
        '''
        [['GiyBTEsXBR', 99.9885090161], ['qISUKItSwC', 99.9805785608], ['bZYQevPKFy', 99.9792039579], ['zTJAhTqNgJ', 99.962903977], ['xvriRtRrvs', 99.8850728073], ['HaXZaHEWIT', 99.8716577729], ['kjxhCdSYyR', 99.8222696379], ['ZpkldiYJLx', 99.7675826054], ['AsTZYwyOTf', 99.7612080507], ['ZorLovUzWJ', 99.6313168876]]
        '''
    queryB = True
    if(queryB):
        cur.execute("""
        Select title,hotness,upvotes,downvotes from lobsters.stories order by upvotes desc, downvotes asc LIMIT 10;
        """)
        print(cur.fetchall())
        '''
        [['CXxOEtHUyp', 19.1955012236, 10, 0], ['FZzvBRTEQL', -96.9180169369, 10, 0], ['WMDJnthHxR', -94.0422849187, 10, 0], ['DdGuGfgMmR', -87.8176832647, 10, 0], ['ZelrXpNakL', 94.4666326731, 10, 0], ['rDefdxZwXE', 45.5148076851, 10, 0], ['csShiBeiUh', -23.7793005072, 10, 0], ['dVfQdzTVDk', 79.3422847424, 10, 0], ['xlqwCAQYTd', 15.0425866041, 10, 0], ['JnjSXezSjL', 91.0533544323, 10, 0]]
        '''
    timeQueries = True
    if(timeQueries):
        st1=time.time()
        cur.execute("""
        Select * from lobsters.stories;
        """)
        end1=time.time()
        st2 = time.time()
        cur.execute("""
        Select id from lobsters.stories;
        """)
        end2=time.time()
        st3=time.time()
        cur.execute("""
        Select id,title from lobsters.stories;
        """)
        end3=time.time()
    print(end1-st1)
    print(end2-st2)
    print(end3-st3)
    cur.execute("""
        select request_duration_ms,request from v_monitor.query_requests limit 10;
    """)
    print(cur.fetchall())

    '''
    run times tend to average around

    71,5,7
      70,5,6
      74,12,7
      69,5,7
      77,5,7
      68,6,7 all in ms
    '''

    # Print the results

    cur.close()
