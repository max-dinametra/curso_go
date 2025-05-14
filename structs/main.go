package main

import (
	"fmt"
)

type contactInfo struct {
	email   string
	zipCode int
}

type person struct {
	firstName string
	lastName  string
	contact   contactInfo
}

func main() {
	//alex := person{firstName: "alex", lastName: "anderson"}
	//fmt.Println(alex)

	// var alex person
	// alex.firstName = "alex"
	// alex.lastName = "anderson"
	// fmt.Println(alex)
	// fmt.Printf("%+v", alex)

	jim := person{
		firstName: "jim",
		lastName:  "party",
		contact: contactInfo{
			email:   "jim@gmail.com,",
			zipCode: 94000,
		},
	}
	//jimPointer := &jim
	jim.updateName("jimmy")
	jim.print()
}

func (pointerToPerson *person) updateName(newFirstName string) {
	(*pointerToPerson).firstName = newFirstName
}

func (p person) print() {
	fmt.Printf("%+v", p)

}
