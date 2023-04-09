# Genrate the first query
prompt ='''Q. Can you me the science keywords for london for last year
A. {"location":"london",
	"start_date": "2022-04-07T00:00:00Z",
	"end_date": "2023-04-07T00:00:00Z",
	"query": "['science_keyword']",
	"science_keyword": "True"
	}
	
Q. Can you give number of datasets present for new york for project or collection or dataset ESI
A. {
	"location": "new york",
	"project" : "ESI",
	"query" : "['number']",
	"science_keyword": "False"
	}
	
Q. Can you give number of dataset present for new york and london for last year
A. 
  [{"location":"london",
	"start_date": "2022-04-07T00:00:00Z",
	"end_date": "2023-04-07T00:00:00Z",
	"query": "['number']",
	"science_keyword": "False"
	},
	{"location":"new york",
	"start_date": "2022-04-07T00:00:00Z"]",
	"end_date": "2023-04-07T00:00:00Z",
	"query": "['number']",
	"science_keyword": "False"
	}]
	
Q. Can you give number of datasets present for new york for collection ESI and science keywords for london for last year
[
   {"location":"new york",
	"start_date": "2022-04-07T00:00:00Z",
	"end_date": "2023-04-07T00:00:00Z",
	"query": "['number']",
	"science_keyword": "False"
   },
   {"location":"london",
	"start_date": "2022-04-07T00:00:00Z",
	"end_date": "2023-04-07T00:00:00Z",
	"query": "['science_keyword']",
	"science_keyword": "True"
   }
]
Q. Can you give me the datasets in climate change for the year 2000 to 2010
A.
	[{"start_date": "2000-01-01T00:00:00Z",
	"end_date": "2011-01-01T00:00:00Z",
	"query": "['climate', 'change']"
	"science_keyword": "True"
	]
	
Q. Can you give me the datasets in climate change, aerosol and temprature for the year 2000 to 2010
A.
	[{"start_date": "2000-01-01T00:00:00Z",
	"end_date": "2011-01-01T00:00:00Z",
	"query": "['climate', 'change', 'aerosol', 'temprature']"
	"science_keyword": "True"
	]'''