# Calendar Desktop Notifier

## Main Feature

The script desktop_notification.py authenticates into a Google calendar and provides a desktop push notification for each upcoming event in the calendar a certain time before each event.

## Instructions to install the application

```bash
git clone 
cd desktop_notifier
conda env create -f environment.yml
conda activate desktop_notifier
```

## Turn on the Google Calendar API

1. Visit this link and click on the button "Enable the Google Calendar API"

2. In resulting dialog click DOWNLOAD CLIENT CONFIGURATION and save the file credentials.json to the project directory.

## Instructions to use the application

```bash
python desktop_notifier.py [TIME_BEFORE_EVENT_MIN]
```

## Limitations

* Only tested in MacOS BigSur and Windows 10;
