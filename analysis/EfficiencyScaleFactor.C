/*
 * Read ROOT files with efficiency measurements from DATA and MC
 * and divide them to calculate a scaling factor.
 */

void EfficiencyScaleFactor(){
    // Set the input/output files of MC and DATA efficiency measurements
    TString inputFile_DATA = "data/MuonTagAndProbe_DATA.root";
    TString inputFile_MC = "data/MuonTagAndProbe_MC.root";
    TString outputFile_SCALE = "data/MuonTagAndProbe_SCALE.root";

    // Set the path in the ROOT files for MC and DATA
    TString inputPath_DATA = "tpTree/MuonEfficiency/fit_eff_plots/pt_PLOT_NewHighPtID_pass_&_tag_IsoMu20_pass";
    TString inputPath_MC = inputPath_DATA;

    // Load efficiency plots from files
    TFile *f_DATA = new TFile(inputFile_DATA);
    TFile *f_MC = new TFile(inputFile_MC);

    TCanvas* c_DATA = (TCanvas*) f_DATA->Get(inputPath_DATA);
    TCanvas* c_MC = (TCanvas*) f_MC->Get(inputPath_MC);
    TGraphAsymmErrors* g_DATA = (TGraphAsymmErrors*) c_DATA->GetPrimitive("hxy_fit_eff");
    TGraphAsymmErrors* g_MC = (TGraphAsymmErrors*) c_MC->GetPrimitive("hxy_fit_eff");

    if(g_DATA->GetN() != g_MC->GetN()) std::cerr << "[ERROR] Number of points of input graphs differ." << std::endl;

    // Divide efficiency graphs to get the scale factor.
    // FIXME: We have to discuss this:
    // We use simple error propagation for division:
    // err_(a/b) / (a/b) = sqrt( (err_a/a)^2 + (err_b/b)^2 )
    // because the measurements are uncorrelated (taken from different data sets)
    // Furthermore, the errors are considered as symmetric.
    Int_t n = g_DATA->GetN();
    TGraphErrors* g_scale = new TGraphErrors(n);

    Double_t x_DATA, x_MC, y_DATA, y_MC, x_scale, y_scale;
    Double_t err_x_DATA, err_x_MC, err_y_DATA, err_y_MC, err_x_scale, err_y_scale;
    for(Int_t i=0; i<n; i++){
        // Get data from input graphs
        g_DATA->GetPoint(i, x_DATA, y_DATA);
        err_x_DATA = g_DATA->GetErrorX(i);
        err_y_DATA = g_DATA->GetErrorY(i);
        g_MC->GetPoint(i, x_MC, y_MC);
        err_x_MC = g_MC->GetErrorX(i);
        err_y_MC = g_MC->GetErrorY(i);

        if(std::abs(x_MC/x_DATA-1)>0.01) std:cerr << "[WARNING] Values on X axis of input graphs differ by " << std::abs(x_MC/x_DATA-1) << " percent." << std::endl;

        // Write to output graph
        x_scale = x_DATA;
        y_scale = y_DATA/y_MC;
        g_scale->SetPoint(i, x_scale, y_scale);

        // This would be the correct error propagation for x, but we set it on the bin width
        // such as done in the original efficiency plots.
        //err_x_scale = x_scale*std::sqrt(std::pow(err_x_DATA/x_DATA,2)+std::pow(err_x_MC/x_MC,2));
        err_x_scale = err_x_DATA;
        err_y_scale = y_scale*std::sqrt(std::pow(err_y_DATA/y_DATA,2)+std::pow(err_y_MC/y_MC,2));
        g_scale->SetPointError(i, err_x_scale, err_y_scale);
    }

    // Write the scale factor graph and the original efficiency graphs to the output ROOT file
    TFile* f_SCALE = new TFile(outputFile_SCALE, "recreate");
    g_scale->SetName("Scale Factor");
    g_scale->SetTitle("Scale Factor");
    g_scale->GetXaxis()->SetTitle(g_DATA->GetXaxis()->GetTitle());
    g_scale->GetYaxis()->SetTitle("Scale Factor");
    g_scale->Write();

    // Clean-up
    f_DATA->Close();
    f_MC->Close();
    f_SCALE->Close();
}
