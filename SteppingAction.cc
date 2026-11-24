#include "SteppingAction.hh"
#include "DetectorConstruction.hh"

#include "G4Step.hh"
#include "G4Track.hh"
#include "G4Gamma.hh"
#include "G4VProcess.hh"
#include "G4AnalysisManager.hh"
#include "G4SystemOfUnits.hh"

SteppingAction::SteppingAction(const DetectorConstruction* det)
  : fDet(det) {}

void SteppingAction::UserSteppingAction(const G4Step* step) {
  auto* track = step->GetTrack();

  if (track->GetParentID() != 0) return;
  if (track->GetDefinition() != G4Gamma::GammaDefinition()) return;

  auto* prePoint  = step->GetPreStepPoint();
  auto* postPoint = step->GetPostStepPoint();

  G4double zExit = 0.5 * fDet->GetSlabThickness();
  G4double zPre  = prePoint->GetPosition().z();
  G4double zPost = postPoint->GetPosition().z();

  if (zPre <= zExit && zPost > zExit) {
    auto* proc = postPoint->GetProcessDefinedStep();
    G4bool hadInteraction = (proc != nullptr &&
                             proc->GetProcessType() == fElectromagnetic &&
                             proc->GetProcessSubType() != 1);

    if (!hadInteraction) {
      auto* analysisManager = G4AnalysisManager::Instance();
      analysisManager->FillNtupleDColumn(0, fDet->GetSlabThickness() / cm);
      analysisManager->FillNtupleDColumn(1, postPoint->GetKineticEnergy() / keV);
      analysisManager->AddNtupleRow();
    }
  }
}
