/*
 * Combine the plots gathered by 'collectPlots.C'.
 */

void comparePlots(TString theFileName1, TString theOutFileName){
    std::cout << "[INFO] Compare plots..." << std::endl;

    TFile *myFile1 = new TFile(theFileName1);
    TFile *myOutFile = new TFile(theOutFileName,"RECREATE");
    TIter nextKey(myFile1->GetListOfKeys());
    TKey *key;

    std::vector<TGraphAsymmErrors * > graphs;
    while ( (key = (TKey*)nextKey()) ){
        TString myName = key->GetName();
        std::cout << "[INFO] Found graph: " << myName << std::endl;
        TGraphAsymmErrors * myGraph = (TGraphAsymmErrors*) myFile1->Get(myName);
        graphs.push_back(myGraph);
    }
    std::cout << "[INFO] Plot " << graphs.size() << " graphs." << std::endl;

    if(graphs.size()>5) std::cout << "[WARNING] Only five different colors are implemented!" << std::endl;
    std::vector<Int_t> colorMap = {kBlue+1, kOrange+7,kRed+1, kGreen+1, kAzure+1};
    std::vector<Int_t> markerMap = {20, 23, 21, 22, 24};
    TCanvas* canvas = new TCanvas("canvasName", "comparePlots", 500, 500);
    canvas->cd();
    TMultiGraph* mg = new TMultiGraph();
    //canvas->SetGrid();
    for (int i=0; i<graphs.size(); i++){
        graphs[i]->SetLineColor(colorMap[i%colorMap.size()]);
        graphs[i]->SetFillColor(colorMap[i%colorMap.size()]);
        graphs[i]->SetMarkerColor(colorMap[i%colorMap.size()]);
        graphs[i]->SetMarkerStyle(markerMap[i%markerMap.size()]);
        graphs[i]->SetMarkerSize(0.8);
        mg->Add(graphs[i]);
    }
    mg->Draw("AP");
    mg->GetYaxis()->SetTitle("Efficiency");
    mg->GetXaxis()->SetTitle(graphs[0]->GetXaxis()->GetTitle());
    myOutFile->cd();
    canvas->Update();
    canvas->Write();

    myOutFile->Close();
}
