MATCH_PAC = (
    """
    MATCH (n:PACAndPartyCommittee)
    WHERE n.committee_name =~ "(?i).*Dropbox.*"
    RETURN n
    Limit 1
    """
)

# MATCH_PAC = (
#     """
#     MATCH (n)
#     RETURN n
#     LIMIT 10
#     """
# )

## Find a way to not need the limit of 100.
MATCH_PAC_ID_COMMITTEE = (
    """
    MATCH (n:Committee{id: 'C00695304'})-[r]-(connectedNode)
    RETURN n, r, connectedNode
    LIMIT 100
    """
) 

# MATCH_PAC = (
#     f"""
#         MATCH (n:PACAndPartyCommittee)
# 	    WHERE n.committee_name =~ “(?i).*{company_name}*”
# 	    RETURN n
#     """
# )

# MATCH_PAC_ID_COMMITTEE = (
#    f"""
#         MATCH (n:Committee{id: {pac_id}})-[r]-(connectedNode)
# 	    RETURN n, r, connectedNode
#     """
# )