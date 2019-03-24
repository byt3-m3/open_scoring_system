PCAP1_QUESTIONS = {
    "event_id": "PCAP1",
    "artifacts": {
        "file": "sec-brutforce.pcapng"
    },
    "questions": [
        {
            "q_id": "PCAP1_1",
            "question": "What protocol is being used to connect to the destination?",
            "answer": "FTP",
            "validation": [
                "Apply filter 'ftp'"
            ]
        },
        {
            "q_id": "PCAP1_2",
            "question": "What is the URL the attacker trying to gain access to?",
            "answer": "creditus.com",
            "validation": [
                "Apply filter 'ftp'",
                "review info column"
            ]
        },
        {
            "q_id": "PCAP1_3",
            "question": "What username is the attacker attempting to use?",
            "answer": "Fred",
            "validation": [
                "right click on ftp packet, click follow tcp stream",
                "Look for 'USER'"
            ]
        },
        {
            "q_id": "PCAP1_4",
            "question": "What type of attack is the user attempt to execute?",
            "answer": "bruteforce",
            "validation": [
                "Based on the number for TCP attempts, this signifies a classic bruteforce"
            ]
        }
    ]
}

PCAP2_QUESTIONS = {
    "event_id": "PCAP2",
    "artifacts": {
        "file": "sec-clientdying.pcapng"
    },
    "questions": [
        {
            "q_id": "PCAP2_1",
            "question": "What is the name of the malicious executable?",
            "answer": "ysbinstall_1000489_3.exe",
            "validation": [
                "Apply filter tcp.stream eq 16 || tcp contains exe",
                "Right click on any packet and select follow TCP stream",
                "Look for “this program cannot run in dos mode”"
            ],
            "point": 25
        },
        {
            "q_id": "PCAP2_2",
            "question": "What is the source IP address of the malicious download?",
            "answer": "216.127.33.119",
            "validation": [
                "Apply filter tcp.stream eq 16 || tcp contains exe",
                "Check Packet 183 ip.destination feild"
            ],
            "point": 25
        },
        {
            "q_id": "PCAP2_3",
            "question": "What is the IP address of the IRC server?",
            "answer": "69.64.34.124",
            "validation": [
                "Apply filter'irc'"
            ],
            "point": 25
        },
        {
            "q_id": "PCAP2_4",
            "question": "For the DNS query,  which flag is set for the hostname www.ysbweb.com?",
            "answer": "Recursion desired: Do query recursively",
            "validation": [
                "apply filter 'dns'",
                "open packet 150",
                "open DNS header",
                "Open Flags",
                "look for 'Recursion desired: Do query recursively'"
            ],
            "point": 25
        }
    ]
}

TEAMS = [
    {
        "name": "team1",
        "passwd": "team1",
        "responses": [],
        "points": 0
    },
    {
        "name": "team2",
        "passwd": "team2",
        "responses": [],
        "points": 0
    },
    {
        "name": "team3",
        "passwd": "team3",
        "responses": [
            {
                "q_id": "PCAP1_1"

            },
            {
                "q_id": "PCAP1_2"

            },

        ],
        "points": 0
    },
    {
        "name": "team4",
        "passwd": "team4",
        "responses": [],
        "points": 0
    },
    {
        "name": "team5",
        "passwd": "team5",
        "responses": [],
        "points": 0
    },
]


def get_team(name):
    for team in TEAMS:
        if team['name'] == name:
            return team
