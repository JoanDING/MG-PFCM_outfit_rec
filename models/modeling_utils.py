from torch import nn, Tensor
import torch
from torchvision.models import resnet18


def initialize_vision_backbone(model: str) -> nn.Module:
    if model == 'resnet18':
        return nn.Sequential(*list(resnet18(pretrained=True).children())[:-2])
    else:
        raise RuntimeError(f'Unrecognized backbone: {model}.')


def init_weights(module: nn.Module):
    """ Initialize the weights """
    if isinstance(module, (nn.Linear, nn.Embedding)):
        # Slightly different from the TF version which uses truncated_normal for initialization
        # cf https://github.com/pytorch/pytorch/pull/5617
        module.weight.data.normal_(mean=0.0, std=0.02)
    elif isinstance(module, nn.LayerNorm):
        module.bias.data.zero_()
        module.weight.data.fill_(1.0)
    if isinstance(module, nn.Linear) and module.bias is not None:
        module.bias.data.zero_()


def weighted_avg(linear: nn.Linear, x: Tensor, mask: Tensor = None):
    scores = linear(x).squeeze(-1)
    if mask is not None:
        scores = scores + (1 - mask).to(scores.dtype) * -10000.0
    alpha = torch.softmax(scores, dim=-1)
    y = torch.einsum("bs,bsh->bh", alpha, x)
    return y
