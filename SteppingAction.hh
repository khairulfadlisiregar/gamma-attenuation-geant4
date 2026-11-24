#ifndef SteppingAction_h
#define SteppingAction_h 1

#include "G4UserSteppingAction.hh"
#include "globals.hh"

class DetectorConstruction;

class SteppingAction : public G4UserSteppingAction {
public:
  explicit SteppingAction(const DetectorConstruction* det);
  ~SteppingAction() override = default;

  void UserSteppingAction(const G4Step* step) override;

private:
  const DetectorConstruction* fDet;
};

#endif
