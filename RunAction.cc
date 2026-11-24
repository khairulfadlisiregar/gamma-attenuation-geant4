#include "RunAction.hh"

#include "G4Run.hh"
#include "G4AnalysisManager.hh"

RunAction::RunAction() {
  auto* analysisManager = G4AnalysisManager::Instance();
  analysisManager->SetDefaultFileType("csv");
  analysisManager->SetNtupleMerging(true);

  analysisManager->CreateNtuple("transmission", "Transmitted Gammas");
  analysisManager->CreateNtupleDColumn("thickness_cm");
  analysisManager->CreateNtupleDColumn("energy_keV");
  analysisManager->FinishNtuple();
}

void RunAction::BeginOfRunAction(const G4Run*) {
  auto* analysisManager = G4AnalysisManager::Instance();
  analysisManager->OpenFile();
}

void RunAction::EndOfRunAction(const G4Run*) {
  auto* analysisManager = G4AnalysisManager::Instance();
  analysisManager->Write();
  analysisManager->CloseFile();
}
