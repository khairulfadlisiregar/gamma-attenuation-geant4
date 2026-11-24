#include "ActionInitialization.hh"
#include "DetectorConstruction.hh"
#include "PrimaryGeneratorAction.hh"
#include "SteppingAction.hh"
#include "RunAction.hh"

ActionInitialization::ActionInitialization(const DetectorConstruction* det)
  : fDet(det) {}

void ActionInitialization::BuildForMaster() const {
  SetUserAction(new RunAction());
}

void ActionInitialization::Build() const {
  SetUserAction(new RunAction());
  SetUserAction(new PrimaryGeneratorAction());
  SetUserAction(new SteppingAction(fDet));
}
