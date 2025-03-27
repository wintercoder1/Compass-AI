from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from cassandra.auth import PlainTextAuthProvider
from cassandra import ConsistencyLevel
from dotenv import find_dotenv, dotenv_values
from typing import Optional
from ssl import SSLContext, PROTOCOL_TLSv1_2,  CERT_NONE
from DataCache import CqlCommands
from DataClassWrappers.TopicInfo import TopicInfo
from QueryTypeEnum import QueryType
from Util import topicInfoFromDict

class CassandraDBCache:

    DEV_LOCALHOST_URL = '127.0.0.1'
    DEV_PORT = '9042'

    def __init__(self, prod=False) -> None:
        # Prod configuration
        if prod:
            dotenv = dotenv_values(find_dotenv())
            PROD_URL = dotenv.get('CASSANDRA_KEY_SPACES_AWS_URL')
            PROD_PORT = dotenv.get('CASSANDRA_KEY_SPACES_AWS_PORT')
            # AWS_CERT_PATH = dotenv.get('AWS_CERT_PATH')
            AWS_KEYSPACES_USER_NAME= dotenv.get('AWS_KEYSPACES_USER_NAME')
            AWS_KEYSPACES_PASSWORD= dotenv.get('AWS_KEYSPACES_PASSWORD')
            ## SSL for AWS cert.
            ssl_context = SSLContext(PROTOCOL_TLSv1_2 )
            # TODO: update this to actualy use cert lol.
            ssl_context.verify_mode = CERT_NONE
            # autprovider
            auth_provider = PlainTextAuthProvider(username=AWS_KEYSPACES_USER_NAME, 
                                                  password=AWS_KEYSPACES_PASSWORD
                                                  )

            cluster = Cluster(
                [PROD_URL], # By default connects to localhost.
                ssl_context=ssl_context, 
                auth_provider=auth_provider, 
                port=PROD_PORT
            )
        else:
            cluster = Cluster(
                [self.DEV_LOCALHOST_URL], # By default connects to localhost.
                port=self.DEV_PORT
            )
        self.session = cluster.connect()
        self.session.row_factory = dict_factory # returns rows as dict
        # Setup
        # These are all with If not exist suffix.
        # If keyspace doesnt exist on localhost create it.
        self.session.execute(CqlCommands.CREATE_DEICHECK_KEYSPACE_WITH_REPLICATION)
        # Set keyspace.
        self.session.set_keyspace(CqlCommands.DEI_CHECK_KEYSPACE_NAME)
        # Create table that will store a list of answers for each topic.
        # Political leaning DEI and Wokeness will all be seperate tables.
        self.session.execute(CqlCommands.CREATE_POLITICAL_LEANING_TABLE)
        self.session.execute(CqlCommands.CREATE_DEI_CHECK_TABLE)
        self.session.execute(CqlCommands.CREATE_WOKENESS_TABLE)
        self.session.execute(CqlCommands.CREATE_FINANCIAL_CONTRIUBTIONS_INFO_TABLE)
        

    # Write:
    def writeTopicInfoToDB(self, topicInfo: TopicInfo):
        # Write LLm answer to the applicate table.
        # ie political leaning to political leaning table. dei or wokeness to respective table.
        # Cassandra managed service requires  local quorum consistency level.
        INSERT = self.session.prepare(CqlCommands.INSERT_POLITICAL_LEANING_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        self.session.execute(INSERT, 
                             (
                                topicInfo.normalized_topic_name, 
                                topicInfo.timestamp, 
                                topicInfo.topic, 
                                topicInfo.lean, 
                                topicInfo.rating, 
                                topicInfo.context, 
                                topicInfo.citation
                            )
        )
        return
    
    def writeTopicInfoToDB_DEI(self, topicInfo: TopicInfo):
        # Write LLm answer to the applicate table.
        # ie political leaning to political leaning table. dei or wokeness to respective table.
        # Cassandra managed service requires  local quorum consistency level.
        INSERT = self.session.prepare(CqlCommands.INSERT_DEI_FRIENDLINESS_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        print(topicInfo)
        self.session.execute(INSERT, 
                             (
                                topicInfo.normalized_topic_name, 
                                topicInfo.timestamp, 
                                topicInfo.topic, 
                                topicInfo.rating, 
                                topicInfo.context, 
                                topicInfo.citation
                            )
        )
        return
    
    def writeTopicInfoToDB_Wokeness(self, topicInfo: TopicInfo):
        # Write LLm answer to the applicate table.
        # ie political leaning to political leaning table. dei or wokeness to respective table.
        # Cassandra managed service requires  local quorum consistency level.
        INSERT = self.session.prepare(CqlCommands.INSERT_WOKENESS_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        print(topicInfo)
        self.session.execute(INSERT, 
                             (
                                topicInfo.normalized_topic_name, 
                                topicInfo.timestamp, 
                                topicInfo.topic, 
                                topicInfo.rating, 
                                topicInfo.context, 
                                topicInfo.citation
                            )
        )
        return
    def writeTopicInfoToDB_FinancialContributions(self, topicInfo: TopicInfo):
        # Write LLm answer to the applicate table.
        INSERT = self.session.prepare(CqlCommands.INSERT_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        self.session.execute(INSERT, 
                             ()
        )
        return

    #
    #
    # Below is test code. Will delete.
    #
    #
    def writeTopicInfoToDB_FinancialContributionsTest(self, topicInfo: TopicInfo):
        # Write LLm answer to the applicate table.
        INSERT = self.session.prepare(CqlCommands.INSERT_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        self.session.execute(INSERT, 
            (
                                'Disney', 
                                'disney', 
                                0, 
                                197749, 
                                -1,
                                """ 
                                Based on the provided FEC data, I can summarize what it reveals about Disney employees' political contributions to the "Cathy McMorris Rodgers for Congress" committee:\n
                                Key Findings\n\n

                                Contributor Profile: The data shows numerous Disney executives and employees making personal contributions to Cathy McMorris Rodgers' campaign, including:\n\n

                                Senior executives (EVPs, SVPs, VPs)\n
                                Department heads across various Disney divisions (Disney+, Walt Disney Studios, Disney Parks, etc.)\n
                                Legal counsel and government relations staff\n\n\n


                                Contribution Pattern:\n\n

                                Contribution amounts range from $60 to $480 per transaction\n
                                Many individuals made multiple contributions (in both January/February 2023 and March/April 2023)\n
                                The data shows a pattern of consistent support from Disney employees across divisions\n\n\n


                                Political Alignment:\n\n

                                Cathy McMorris Rodgers is a Republican congresswoman from Washington state\n
                                She has served as Chair of the House Republican Conference and on the House Energy and Commerce Committee\n
                                The contributions indicate support from Disney employees for a Republican candidate\n\n\n


                                Corporate Representation:\n\n

                                Contributors come from diverse Disney business units including:\n\n

                                Disney Studios\n
                                Disney+\n
                                Disney Parks, Experiences and Products\n
                                ESPN\n
                                Disney Media and Entertainment Distribution\n
                                Disney General Entertainment\n
                                Walt Disney World\n\n\n\n\n





                                Political Implications\n
                                These contributions suggest that despite Disney's public positioning on certain social issues, many of its executives and upper-level employees personally support Republican candidates. This demonstrates a more complex political landscape within the company than might be assumed from the company's public positions.\n
                                It's important to note that these are individual contributions, not direct corporate donations. However, the pattern of support from employees at executive levels could reflect aspects of the company's internal political culture, particularly among leadership.\n
                                The data doesn't necessarily indicate Disney as a company's overall political leaning, but rather shows significant Republican support among its executive ranks who chose to make personal political contributions to this specific campaign.\n\n
                                
                                """, 
                                'Anthropic Claude Sonnet 3.7 (Manual entry)', 
                                '2025-03-20'
                            ) 
        )
        return
    
    def writeTopicInfoToDB_FinancialContributionsTestSony(self):
        # Write LLm answer to the applicate table.
        INSERT = self.session.prepare(CqlCommands.INSERT_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        self.session.execute(INSERT, 
        #                     (

        #                     )
        # )
                             (
                                'Sony Pictures', 
                                'sonypictures', 
                                0, 
                                282828, 
                                -1,
                                """ 
                                Overview of Sony Pictures' Political Contributions
                                The data shows contributions from Sony Pictures Entertainment executives through a PAC named "SYDNEY KAMLAGER-DOVE FOR CONGRESS" (ID: C00282038). This PAC makes contributions to various political candidates and their campaigns.
                                Contribution Patterns
                                Contributor Demographics

                                All contributors in the data are identified as "EXECUTIVE" at Sony Pictures Entertainment
                                Contributors include: Jeffrey Korchek, Lexine Wong, Jason K Spivak, Arthur Shapiro, Flory Bramnick, Ann-Elizabeth Gorski, Lucienne Hassler, Sean Jaquez, Sean Miller, Zachary McGee, Paul Martin, Michael Marshall, and Marie Jacobson

                                Contribution Amounts

                                Individual contribution amounts ranged from $38 to $192
                                Multiple executives made repeated contributions across different months in 2023 (February, April)

                                Political Recipients
                                The PAC associated with these Sony executives contributed to various campaigns across both political parties:
                                Democratic Recipients

                                Sydney Kamlager-Dove (CA-37)
                                Val Hoyle (OR)
                                Gabe Vasquez (NM)
                                Pat Ryan (NY)
                                Jamaal Bowman (NY)
                                Christopher Coons (DE, Senate)
                                Martin Heinrich (NM, Senate)

                                Republican Recipients

                                Kelly Armstrong (ND)
                                Jay Obernolte (CA-23)
                                Mike Bost (IL)
                                Michelle Steel (CA-45)
                                Darrell Issa (CA-48)
                                Laurel Lee (FL-15)

                                Political Leaning Analysis
                                The contribution pattern suggests Sony Pictures maintains a bipartisan political giving strategy:

                                Balanced Approach: The PAC contributed to both Democratic and Republican candidates, indicating a strategic bipartisan approach rather than strict ideological alignment.
                                Pragmatic Business Strategy: The distribution of contributions suggests Sony Pictures likely supports candidates based on their committee assignments, influence in the entertainment industry, and positions on issues relevant to the company's business interests, regardless of party.
                                Geographic Focus: Many contributions went to California representatives, where Sony Pictures is headquartered (Culver City), suggesting the company prioritizes relationships with local representatives who directly impact their operations.
                                Contribution Timing: The contributions appear to be strategically timed for both primary and general elections across the 2023-2024 election cycle.

                                The data indicates Sony Pictures Entertainment maintains a politically pragmatic approach, supporting candidates from both major parties who may be influential on policies affecting the entertainment industry. Rather than showing a clear partisan lean, the contribution pattern suggests the company pursues a balanced political strategy designed to maintain relationships across the political spectrum.RetryClaude can make mistakes. Please double-check responses. 3.7 Sonnet
                                """, 
                                'Anthropic Claude Sonnet 3.7 (Manual entry)', 
                                '2025-03-20'
                            ) 
        )
        return
    

    def writeTopicInfoToDB_FinancialContributionsTestDropBox__(self):
        # Write LLm answer to the applicate table.
        INSERT = self.session.prepare(CqlCommands.INSERT_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        self.session.execute(INSERT, 
        #                     (

        #                     )
        # )
                             (
                                'Dropbox', 
                                'dropbox', 
                                0, 
                                60684, 
                                -1,
                                """ 
                                Political Contributions Analysis for Dropbox

                                Based on the data, there appears to be a Political Action Committee (PAC) called "THOM TILLIS COMMITTEE" (ID: C00695304) that received contributions from several Dropbox executives and employees during 2023. Let me break down what this reveals about Dropbox's political leanings:
                                Key Contributors from Dropbox
                                Several high-ranking Dropbox employees made contributions to this PAC:

                                Bart Volkmer (Chief Legal Officer) - $5,000
                                Andrew Houston (CEO) - $5,000
                                Amber Cottle (Head of Public Policy) - Multiple contributions of $556
                                Lisa Youel (Global Head of Tax) - $200 (multiple contributions)
                                Matthew Jezorek (Sr. Director, Security Engineering) - $200 (multiple contributions)
                                David Stafford (Sr. Director GSS) - $100 (multiple contributions)
                                Saman Asheer (VP, Communications) - $200 (multiple contributions)

                                Contribution Patterns and Political Leaning
                                The PAC (THOM TILLIS COMMITTEE) made contributions to candidates from both major political parties:
                                Republican Recipients:

                                Thom Tillis (NC Senator)
                                Dan Sullivan (AK Senator)
                                Jay Obernolte (CA Representative)
                                John Curtis (UT Representative)
                                Kat Cammack (FL Representative)
                                Juan Ciscomani (AZ Representative)
                                Todd Young (IN Senator)
                                Kelly Armstrong (ND Representative)

                                Democratic Recipients:

                                Brian Schatz (HI Senator)
                                Gary Peters (MI Senator)
                                Doris Matsui (CA Representative)
                                Yvette Clarke (NY Representative)
                                Marc Veasey (TX Representative)
                                Elizabeth Fletcher (TX Representative)
                                Alex Padilla (CA Senator)
                                Christopher Coons (DE Senator)

                                Conclusion on Political Leanings
                                The data suggests that Dropbox executives and the associated PAC demonstrate bipartisan political giving. While contributions come from Dropbox's leadership team, the PAC's distribution of funds shows support for both Republican and Democratic candidates across multiple states.
                                This bipartisan approach is common among technology companies that aim to maintain relationships with lawmakers on both sides of the aisle to address issues relevant to their business interests like data privacy, intellectual property, and technology regulation. Rather than showing a distinct partisan leaning, the contribution pattern suggests Dropbox is primarily focused on cultivating political relationships that may benefit their business operations regardless of party affiliation.
                                The geographic diversity of supported candidates (spanning California, North Carolina, Texas, Hawaii, Michigan, etc.) further supports the interpretation that Dropbox's political giving strategy is aimed at broad influence rather than ideological alignment with either major political party.
                                """, 
                                'Anthropic Claude Sonnet 3.7 (Manual entry)', 
                                '2025-03-20'
                            ) 
        )
        return
    
    def writeTopicInfoToDB_FinancialContributionsTestDropBox(self):
        # Write LLm answer to the applicate table.
        INSERT = self.session.prepare(CqlCommands.INSERT_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        self.session.execute(INSERT, 
        #                     (

        #                     )
        # )
                             (
                                'Dropbox', 
                                'dropbox', 
                                0, 
                                60684, 
                                -1,
                                """ 
                                Political Contributions Analysis for Dropbox

                                Based on the data, there appears to be a Political Action Committee (PAC) called "THOM TILLIS COMMITTEE" (ID: C00695304) that received contributions from several Dropbox executives and employees during 2023. Let me break down what this reveals about Dropbox's political leanings:
                                Key Contributors from Dropbox
                                Several high-ranking Dropbox employees made contributions to this PAC:

                                Bart Volkmer (Chief Legal Officer) - $5,000
                                Andrew Houston (CEO) - $5,000
                                Amber Cottle (Head of Public Policy) - Multiple contributions of $556
                                Lisa Youel (Global Head of Tax) - $200 (multiple contributions)
                                Matthew Jezorek (Sr. Director, Security Engineering) - $200 (multiple contributions)
                                David Stafford (Sr. Director GSS) - $100 (multiple contributions)
                                Saman Asheer (VP, Communications) - $200 (multiple contributions)

                                Contribution Patterns and Political Leaning
                                The PAC (THOM TILLIS COMMITTEE) made contributions to candidates from both major political parties:
                                Republican Recipients:

                                Thom Tillis (NC Senator)
                                Dan Sullivan (AK Senator)
                                Jay Obernolte (CA Representative)
                                John Curtis (UT Representative)
                                Kat Cammack (FL Representative)
                                Juan Ciscomani (AZ Representative)
                                Todd Young (IN Senator)
                                Kelly Armstrong (ND Representative)

                                Democratic Recipients:

                                Brian Schatz (HI Senator)
                                Gary Peters (MI Senator)
                                Doris Matsui (CA Representative)
                                Yvette Clarke (NY Representative)
                                Marc Veasey (TX Representative)
                                Elizabeth Fletcher (TX Representative)
                                Alex Padilla (CA Senator)
                                Christopher Coons (DE Senator)

                                Conclusion on Political Leanings
                                The data suggests that Dropbox executives and the associated PAC demonstrate bipartisan political giving. While contributions come from Dropbox's leadership team, the PAC's distribution of funds shows support for both Republican and Democratic candidates across multiple states.
                                This bipartisan approach is common among technology companies that aim to maintain relationships with lawmakers on both sides of the aisle to address issues relevant to their business interests like data privacy, intellectual property, and technology regulation. Rather than showing a distinct partisan leaning, the contribution pattern suggests Dropbox is primarily focused on cultivating political relationships that may benefit their business operations regardless of party affiliation.
                                The geographic diversity of supported candidates (spanning California, North Carolina, Texas, Hawaii, Michigan, etc.) further supports the interpretation that Dropbox's political giving strategy is aimed at broad influence rather than ideological alignment with either major political party.
                                """, 
                                'Anthropic Claude Sonnet 3.7 (Manual entry)', 
                                '2025-03-20'
                            ) 
        )
        return
    
    def writeTopicInfoToDB_FinancialContributionsTestCiti(self):
        # Write LLm answer to the applicate table.
        INSERT = self.session.prepare(CqlCommands.INSERT_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED)
        INSERT.consistency_level = ConsistencyLevel.LOCAL_QUORUM
        self.session.execute(INSERT, 
        #                     (

        #                     )
        # )
                             (
                                'Citi', 
                                'citi', 
                                0, 
                                50498, 
                                -1,
                                """ 
                                The data shows political contributions from Citigroup employees to the "WICKER FOR SENATE" campaign, which is a PAC supporting Senator Roger Wicker from Mississippi (indicated by the MS state code). Senator Wicker is a Republican, so these contributions are supporting a Republican candidate.\n
                                Key observations from the data:\n\n

                                Contributor Demographics:\n\n

                                Contributors are primarily Managing Directors and Directors at Citigroup subsidiaries including Citigroup Global Markets, Citibank N.A., and Citigroup Technology Inc.\n
                                Most contributors are based in New York, with others from locations like Washington DC, Chicago, Miami, and Jersey City.\n


                                Contribution Patterns:\n\n

                                Contribution amounts vary, with common values being $192, $135, $100, $95, $50, and smaller amounts like $29-$40.\n
                                The contributions were primarily made in March-April 2023, with many recorded on March 31, 2023.\n


                                Political Implications:\n\n

                                All contributions in this dataset are to a Republican candidate (Senator Wicker).\n
                                These donations represent one slice of Citigroup's potential political activity, focused on one specific candidate.\n


                                Organizational Structure:\n\n

                                The contributions come from individual employees across different Citigroup entities rather than directly from a corporate PAC.\n
                                Many senior executives (Managing Directors) are contributing, which might indicate some level of coordination or encouragement within the company.\n



                                Without seeing comparable data about potential contributions to Democratic candidates, it's difficult to make a definitive statement about Citigroup's overall political leanings. This dataset only shows contributions to a Republican candidate, but major financial institutions typically make contributions across party lines to maintain relationships with elected officials on both sides of the aisle.\n
                                To fully assess Citigroup's political leanings, we would need to see:\n

                                The full range of PAC donations to candidates of both parties\n
                                Total contribution amounts to Republican vs. Democratic candidates\n
                                Contributions over multiple election cycles\n

                                This dataset provides evidence of support for at least one Republican candidate, but doesn't tell the complete story of Citigroup's political contribution strategy.""", 
                                'Anthropic Claude Sonnet 3.7 (Manual entry)', 
                                '2025-03-20'
                            ) 
        )
        return
    
    # Read:
    # Fetch answers.

    # Returns one most recent answer on topic.
    def fetchInfoOnTopicMostRecent(self, normalized_topic_name: str, queryType: QueryType = QueryType.POLITCAL_LEANING) -> Optional[TopicInfo]: #TopicInfo: #Optional[DataClassWrappers.TopicInfo]:
        # search respective table for an answer relating to the topic.
        if queryType == QueryType.POLITCAL_LEANING:
            FETCH = self.session.prepare(CqlCommands.FETCH_POLITICAL_LEANING_INFO_MOST_RECENT_PREPARED)
        elif queryType == QueryType.DEI_FRIENDLINESS:
            FETCH = self.session.prepare(CqlCommands.FETCH_DEI_FRIENDLINESS_INFO_MOST_RECENT_PREPARED)
        elif queryType == QueryType.WOKENESS:
            FETCH = self.session.prepare(CqlCommands.FETCH_WOKENESS_INFO_MOST_RECENT_PREPARED)
        elif queryType == QueryType.FINANCIAL_CONTRIBUTIONS:
            FETCH = self.session.prepare(CqlCommands.FETCH_FINANCIAL_CONTRIUBTIONS_INFO_MOST_RECENT_PREPARED)
        rows = self.session.execute(FETCH, (normalized_topic_name, ) )
        if not rows:
            return None
        return topicInfoFromDict(row_dict=rows[0], queryType=queryType) 
    
    # Returns all answers ever for topic.
    def fetchInfoOnTopic(self, normalized_topic_name: str, queryType: QueryType = QueryType.POLITCAL_LEANING) -> list:
        if queryType == QueryType.POLITCAL_LEANING:
            FETCH = self.session.prepare(CqlCommands.FETCH_POLITICAL_LEANING_INFO_PREPARED)
        elif queryType == QueryType.DEI_FRIENDLINESS:
            FETCH = self.session.prepare(CqlCommands.FETCH_DEI_FRIENDLINESS_INFO_PREPARED)
        elif queryType == QueryType.WOKENESS:
            FETCH = self.session.prepare(CqlCommands.FETCH_WOKENESS_INFO_PREPARED)
        elif queryType == QueryType.FINANCIAL_CONTRIBUTIONS:
            FETCH = self.session.prepare(CqlCommands.FETCH_FINANCIAL_CONTRIUBTIONS_INFO_PREPARED)
        rows = self.session.execute(FETCH, (normalized_topic_name, ) )
        return rows
    
    # Returns all answers on all topics saved in database.
    def fetchInfoAllTopics(self, queryType: QueryType) -> list:
        if queryType == QueryType.POLITCAL_LEANING:
            COMMAND = CqlCommands.FETCH_POLITICAL_LEANING_INFO
        elif queryType == QueryType.DEI_FRIENDLINESS:
            COMMAND = CqlCommands.FETCH_DEI_FRIENDLINESS_INFO
        elif queryType == QueryType.WOKENESS:
            COMMAND = CqlCommands.FETCH_WOKENESS_INFO
        elif queryType == QueryType.FINANCIAL_CONTRIBUTIONS:
            COMMAND = CqlCommands.FETCH_FINANCIAL_CONTRIUBTIONS_INFO
        rows = self.session.execute(COMMAND)
        print('rows')
        print(rows)
        return rows