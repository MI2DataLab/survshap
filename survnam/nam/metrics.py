"""the calculation of metrics"""

import torch.nn.functional as F
import torch


def feature_loss(fnn_out, lambda_=0.0):
    return lambda_ * (fnn_out**2).sum() / fnn_out.shape[1]


def penalized_cross_entropy(logits, truth, fnn_out, feature_penalty=0.0):
    # regression loss + L2 regularization loss
    return F.binary_cross_entropy_with_logits(
        logits.view(-1), truth.view(-1)
    ) + feature_loss(fnn_out, feature_penalty)


def penalized_mse(logits, truth, fnn_out, feature_penalty=0.0):
    # regression loss + L2 regularization loss
    return F.mse_loss(logits.view(-1), truth.view(-1)) + feature_loss(
        fnn_out, feature_penalty
    )


def survnam_loss(logits, truths, times, baseline, weight):
    return torch.mul(
        torch.sum(
            torch.mul(
                torch.pow(
                    torch.subtract(
                        torch.subtract(
                            torch.log(truths + 0.1), torch.log(baseline + 0.1)
                        ),
                        torch.sum(logits),
                    ),
                    2,
                ),
                torch.diff(times),
            )
        ),
        weight,
    )


def calculate_metric(logits, truths, regression=True):
    """Calculates the evaluation metric."""
    if regression:
        return (
            "MAE",
            ((logits.view(-1) - truths.view(-1)).abs().sum() / logits.numel()).item(),
        )
    else:
        return "accuracy", accuracy(logits, truths)


def accuracy(logits, truths):
    return (
        ((truths.view(-1) > 0) == (logits.view(-1) > 0.5)).sum() / truths.numel()
    ).item()
