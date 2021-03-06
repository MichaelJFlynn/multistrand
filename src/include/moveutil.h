/*
Copyright (c) 2017 California Institute of Technology. All rights reserved.
Multistrand nucleic acid kinetic simulator
help@multistrand.org
*/

// Contains all move-related utility as a base-class.
#ifndef __MOVEUTIL_H__
#define __MOVEUTIL_H__

#include <string>
#include <vector>
#include <map>
#include <sequtil.h>

using std::vector;
using std::string;
using std::map;

class StrandComplex;
class EnergyModel;

enum MoveType {
	endMove, loopMove, stackMove, stackStackMove, loopEndMove, stackEndMove, stackLoopMove, MOVETYPE_SIZE
};

enum QuartContext {
	endC, strandC, stackC, HALFCONTEXT_SIZE
};

namespace moveutil {

MoveType combineBi(QuartContext&, QuartContext&);

const static double valuesPrime[MOVETYPE_SIZE + 1] = { 3, 5, 7, 11, 13, 17, 19, 999 };
const static string MoveToString[MOVETYPE_SIZE] = { "End", "Loop", "Stack", "StackStack", "LoopEnd", "StackEnd", "StackLoop" };
const static string MoveToString2[MOVETYPE_SIZE] = { "       ", "      ", "     ", "", "   ", "  ", " " };

int getPrimeCode(MoveType, MoveType);
string primeToDesc(int);

QuartContext getContext(char input);

int typeMult(MoveType left, MoveType right);

}

// UTILITY STRUCTS

struct HalfContext {

	HalfContext();
	HalfContext(QuartContext, QuartContext);
	friend std::ostream& operator<<(std::ostream&, HalfContext&);
	bool operator==(const HalfContext& other) const;
	bool operator<(const HalfContext&) const;

	QuartContext left = endC;
	QuartContext right = endC;

};

struct JoinCriteria {

	JoinCriteria();
	friend std::ostream& operator<<(std::ostream&, JoinCriteria&);

	StrandComplex* complexes[2] = { NULL, NULL };
	char types[2] = { 0, 0 };
	int index[2] = { 0, 0 };

	// arrhenius rates only
	HalfContext half[2] = { HalfContext(), HalfContext() };
	int arrType = 0; // used for returning the chosen movetype.

};

// This struct contains info computed
// at-time-of-creation for the OpenLoop object.

struct OpenInfo {

public:
	friend std::ostream& operator<<(std::ostream&, OpenInfo&);
	void clear(void);
	void increment(QuartContext, char, QuartContext);
	void increment(HalfContext, BaseCount&);
	void increment(OpenInfo&);

	void decrement(HalfContext, BaseCount&);
	void decrement(OpenInfo&);

	double crossRate(OpenInfo&, EnergyModel&);

	map<HalfContext, BaseCount> tally;

	int numExposedInternal = 0;
	int numExposed = 0;

	bool upToDate = false;

};


#endif
