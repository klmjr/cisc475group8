import {
  Component,
  ChangeDetectionStrategy,
  ViewChild,
  TemplateRef,
  OnInit,
} from '@angular/core';
import {
  startOfDay,
  endOfDay,
  subDays,
  addDays,
  endOfMonth,
  isSameDay,
  isSameMonth,
  addHours,
} from 'date-fns';
import { Subject } from 'rxjs';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import {
  CalendarEvent,
  CalendarEventAction,
  CalendarEventTimesChangedEvent,
  CalendarView,
} from 'angular-calendar';
import data from "../data.json";
//import { writeFileSync } from 'fs';
import firebase from "firebase/app";
import "firebase/database";
//var firebase = require("firebase/app");

const colors: any = {
  red: {
    primary: '#ad2121',
    secondary: '#FAE3E3',
  },
  blue: {
    primary: '#1e90ff',
    secondary: '#D1E8FF',
  },
  yellow: {
    primary: '#e3bc08',
    secondary: '#FDF1BA',
  },
};


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  //data: [{[key: string]:string}] = require("../data.json");
  title = 'ssl-calendar';
  
  //Creates a date component
  view: CalendarView = CalendarView.Month;

  CalendarView = CalendarView;

  viewDate: Date = new Date();

  modalData: {
    action: string;
    event: CalendarEvent;
  };

  actions: CalendarEventAction[] = [
    {
      label: '<i class="fas fa-fw fa-pencil-alt"></i>',
      a11yLabel: 'Edit',
      onClick: ({ event }: { event: CalendarEvent }): void => {
        this.handleEvent('Edited', event);
      },
    },
    {
      label: '<i class="fas fa-fw fa-trash-alt"></i>',
      a11yLabel: 'Delete',
      onClick: ({ event }: { event: CalendarEvent }): void => {
        this.events = this.events.filter((iEvent) => iEvent !== event);
        console.log(this.events);
        this.handleEvent('Deleted', event);
      },
    },
  ];

  refresh: Subject<any> = new Subject();

  //Creates component for drop down menu
  public dropDownValue = "";
      SetDropDownValue(drpValue : any) {
        this.dropDownValue = drpValue.target.value;
      if(this.dropDownValue == "Red"){
        this.events = this.revents;
      }
      else if(this.dropDownValue == "Blue"){
        this.events = this.bevents;
      }
      else if(this.dropDownValue == "White"){
        this.events = this.wevents;
      }
      else{
        this.events = this.testevents;
      }
    }

  revents: CalendarEvent[] = [
    {
      start: subDays(startOfDay(new Date()), 1),
      title: 'A 3 day event',
      color: colors.red,


    },
  ]

  bevents: CalendarEvent[] = [
    {
      start: subDays(startOfDay(new Date()), 1),
      title: 'A 3 day event',
      color: colors.blue,


    },
  ]

  wevents: CalendarEvent[] = [
    {
      start: subDays(startOfDay(new Date()), 1),
      title: 'A 3 day event',
      color: colors.red,


    },
  ]
  events: CalendarEvent[] = 
  [

  ]
  testevents: CalendarEvent[] = [
    
   /* {
      start: subDays(startOfDay(new Date()), 1),
      end: addDays(new Date(), 1),
      title: 'A 3 day event',
      color: colors.red,
      actions: this.actions,
      allDay: true,
      resizable: {
        beforeStart: true,
        afterEnd: true,
      },
      draggable: true,
    },
    {
      start: startOfDay(new Date()),
      title: 'An event with no end date',
      color: colors.yellow,
      actions: this.actions,
    },
    {
      start: subDays(endOfMonth(new Date()), 3),
      end: addDays(endOfMonth(new Date()), 3),
      title: 'A long event that spans 2 months',
      color: colors.blue,
      allDay: true,
    },
    {
      start: addHours(startOfDay(new Date()), 2),
      end: addHours(new Date(), 2),
      title: 'A draggable and resizable event',
      color: colors.yellow,
      actions: this.actions,
      resizable: {
        beforeStart: true,
        afterEnd: true,
      },
      draggable: true,
    },
    */
  ];

  activeDayIsOpen: boolean = true;

  constructor(private modal: NgbModal) {}
  ngOnInit(): void{
    var config = {
      apiKey: "API_KEY",
      authDomain: "calendar-66a80.firebaseapp.com",
      // For databases not in the us-central1 location, databaseURL will be of the
      // form https://[databaseName].[region].firebasedatabase.app.
      // For example, https://your-database-123.europe-west1.firebasedatabase.app
      databaseURL: "https://calendar-66a80-default-rtdb.firebaseio.com/",
      storageBucket: "bucket.appspot.com"
    };
    
    firebase.initializeApp(config);
  
    // Get a reference to the database service
    var database = firebase.database();
    firebase.database().ref().get().then((snapshot)=>{
      if (snapshot.exists()) {
        var datas = snapshot.val();
        console.log(datas);
        datas.forEach(element => {
          this.events.push({
            start: new Date(element.start),
            title: element.title,
            color: colors[element.meta],
            allDay: element.allDay,
            resizable: element.resizable,
            draggable: element.draggable,
            actions: this.actions,
            meta: element.meta
          });
        });
      } else {
        console.log("No data available");
      }
    });
    this.refresh.next();
    /*data.forEach(element => {
      this.events.push({
        start: subDays(startOfDay(new Date(element.start)),1),
        title: element.title,
        color: colors[element.color],
        allDay: element.allDay,
        resizable: element.resizable,
        draggable: element.draggable,
        actions: this.actions
      });
    });*/
  }
  dayClicked({ date, events }: { date: Date; events: CalendarEvent[] }): void {
    if (isSameMonth(date, this.viewDate)) {
      if (
        (isSameDay(this.viewDate, date) && this.activeDayIsOpen === true) ||
        events.length === 0
      ) {
        this.activeDayIsOpen = false;
      } else {
        this.activeDayIsOpen = true;
      }
      this.viewDate = date;
    }
  }

  eventTimesChanged({
    event,
    newStart,
    newEnd,
  }: CalendarEventTimesChangedEvent): void {
    this.events = this.events.map((iEvent) => {
      if (iEvent === event) {
        return {
          ...event,
          start: newStart,
          end: newEnd,
        };
      }
      return iEvent;
    });
    this.save();
    console.log(this.events);
    //fs.writeFileSync("../test.json",this.events);
    //this.handleEvent('Dropped or resized', event);
  }

  handleEvent(action: string, event: CalendarEvent): void {
    this.modalData = { event, action };
    console.log(event);
  }

  addEvent(): void {
    this.events = [
      ...this.events,
      {
        title: 'New event',
        start: startOfDay(new Date()),
        allDay: true,
        color: colors.red,
        actions: this.actions,
        draggable: true,
        resizable: {
          beforeStart: true,
          afterEnd: true,
        },
        meta: "red"
      },
    ];
  }
  save(): void {
    //firebase.database().ref().set(this.events);
    var res = [];
    this.events.forEach(element => {
      res.push({
        start: this.getdate(element.start),
        title: element.title,
        allDay: element.allDay,
        resizable: element.resizable,
        draggable: element.draggable,
        meta: element.meta
      })
    });
    firebase.database().ref().set(res);
    console.log(this.getdate(this.events[0].start));
  }

  deleteEvent(eventToDelete: CalendarEvent) {
    this.events = this.events.filter((event) => event !== eventToDelete);
    console.log(this.events);
  }

  setView(view: CalendarView) {
    this.view = view;
  }

  closeOpenMonthViewDay() {
    this.activeDayIsOpen = false;
  }
  getdate(date:Date): String{
    var month = '' + (date.getMonth() + 1),
        day = '' + date.getDate(),
        year = date.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
  }
}
